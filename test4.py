import paramiko
import os

# Détails de connexion au VPS
vps_ip = "66.63.187.70"
vps_user = "root"
vps_password = "2!4HKS99!usJ49"

# Liste des noms de domaine à configurer
domains = ["contravention-constat.com"]

# Dossier local contenant les fichiers PHP, CSS et images
local_directory = "rbc_info"  # Chemin vers le dossier local contenant les fichiers à transférer

# Dossier distant où les fichiers seront transférés (même pour tous les domaines)
remote_directory = "/var/www/html/"

# Commandes pour vérifier si les paquets sont installés
check_commands = {
    "apache2": "dpkg -l | grep apache2",
    "php": "dpkg -l | grep php",
    "certbot": "dpkg -l | grep certbot",
    "pdo_mysql": "php -m | grep pdo_mysql"  # Vérifie si PDO MySQL est activé
}

# Commandes pour installer Apache, PHP, Certbot et PDO MySQL
install_commands = {
    "apache2": "sudo DEBIAN_FRONTEND=noninteractive apt-get install apache2 -y",
    "php": "sudo DEBIAN_FRONTEND=noninteractive apt-get install php libapache2-mod-php php-curl -y",
    "certbot": "sudo DEBIAN_FRONTEND=noninteractive apt-get install certbot python3-certbot-apache -y",
    "pdo_mysql": "sudo DEBIAN_FRONTEND=noninteractive apt-get install php-mysql -y",
    "ufw": "sudo ufw allow 3001"  # Commande pour ouvrir le port 3001 dans le pare-feu
}

# Fonction pour exécuter une commande via SSH
def run_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    stdout_str = stdout.read().decode()
    stderr_str = stderr.read().decode()
    
    if stderr_str:
        print(f"Erreur lors de l'exécution de '{command}': {stderr_str.strip()}")
    
    return stdout_str, stderr_str

# Fonction pour vérifier si un paquet est installé
def is_installed(client, package_name):
    check_command = check_commands.get(package_name)
    if check_command:
        stdout, stderr = run_command(client, check_command)
        return package_name in stdout
    return False

# Fonction pour vérifier si SSL est activé pour un domaine
def is_ssl_enabled(client, domain):
    stdout, stderr = run_command(client, f"sudo ls /etc/letsencrypt/live/{domain}")
    return "privkey.pem" in stdout

# Vérifier si les fichiers SSL sont générés
def are_ssl_files_present(client, domain):
    ssl_files = ["/fullchain.pem", "/privkey.pem"]
    for file in ssl_files:
        file_path = f"/etc/letsencrypt/live/{domain}{file}"
        stdout, stderr = run_command(client, f"sudo test -f {file_path} && echo 'OK' || echo 'Missing'")
        if "Missing" in stdout:
            print(f"Fichier SSL manquant : {file_path}")
            return False
    return True

# Fonction pour transférer les fichiers en préservant la structure des répertoires
def upload_files_with_structure(sftp, local_path, remote_path):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(root, local_path)
            remote_dir = os.path.join(remote_path, relative_path).replace("\\", "/")
            
            try:
                sftp.chdir(remote_dir)
            except IOError:
                sftp.mkdir(remote_dir)
                sftp.chdir(remote_dir)
            
            remote_file = os.path.join(remote_dir, file).replace("\\", "/")
            try:
                sftp.put(local_file, remote_file)
                print(f"Transfert réussi: {local_file} -> {remote_file}")
            except Exception as e:
                print(f"Erreur lors du transfert du fichier {local_file} vers {remote_file}: {e}")

# Fonction pour remplacer les occurrences de l'IP, du port et de ws par wss
def replace_ip_and_port_in_files(directory, domain, old_port, new_port):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.lower().endswith(ext) for ext in image_extensions):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = content.replace('127.0.0.1', domain)  # Remplacer l'IP par le domaine
                content = content.replace(str(old_port), str(new_port))  # Remplacer le port
                content = content.replace('ws://', 'wss://')  # Remplacer ws par wss
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Remplacement dans le fichier {file_path} effectué.")
            except Exception as e:
                print(f"Erreur lors de la modification du fichier {file_path}: {e}")

# Fonction pour configurer un domaine
def setup_domain(client, domain):
    certbot_command = f"sudo certbot --apache -d {domain} --non-interactive --agree-tos --register-unsafely-without-email"

    vhost_http_config = f"""
    <VirtualHost *:80>
        ServerName {domain}
        DocumentRoot {remote_directory}
        <Directory {remote_directory}>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>
        ErrorLog /var/log/apache2/error.log
        CustomLog /var/log/apache2/access.log combined

        # Redirection HTTP vers HTTPS
        RewriteEngine On
        RewriteRule ^/?(.*) https://%{{HTTP_HOST}}/$1 [R=301,L]
    </VirtualHost>
    """

    vhost_https_config = f"""
    <VirtualHost *:443>
        ServerName {domain}
        DocumentRoot {remote_directory}
        <Directory {remote_directory}>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>
        SSLEngine on
        SSLCertificateFile /etc/letsencrypt/live/{domain}/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/{domain}/privkey.pem

        # Configuration pour WebSocket
        RewriteEngine On
        RewriteCond %{{HTTP:Upgrade}} websocket [NC]
        RewriteCond %{{HTTP:Connection}} upgrade [NC]
        RewriteRule /(.*) wss://{domain}:3001/$1 [P,L]  # Utiliser le domaine pour le WS
        ErrorLog /var/log/apache2/error.log
        CustomLog /var/log/apache2/access.log combined
    </VirtualHost>
    """

    vhost_http_path = f"/etc/apache2/sites-available/{domain}.conf"
    sftp = client.open_sftp()
    try:
        with sftp.open(vhost_http_path, 'w') as f:
            f.write(vhost_http_config)

        if not is_ssl_enabled(client, domain):
            # Commande pour générer un certificat SSL
            stdout, stderr = run_command(client, certbot_command)
            if "Error" in stdout or "Error" in stderr:
                print(f"Erreur lors de la configuration de SSL pour {domain}: {stdout.strip()} {stderr.strip()}")

            # Vérifier si les fichiers SSL existent
            if are_ssl_files_present(client, domain):
                vhost_https_path = f"/etc/apache2/sites-available/{domain}-ssl.conf"
                with sftp.open(vhost_https_path, 'w') as f:
                    f.write(vhost_https_config)

                run_command(client, f"sudo a2ensite {domain}-ssl")
                run_command(client, "sudo systemctl reload apache2")
            else:
                print(f"Les fichiers SSL n'ont pas été générés pour {domain}. Vérifiez la configuration DNS et réessayez.")
    except Exception as e:
        print(f"Erreur lors de la configuration du domaine {domain}: {e}")

# Fonction principale pour configurer tous les domaines
def setup_vps():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps_ip, username=vps_user, password=vps_password)

        # Ouvrir le port 3001 dans le pare-feu
        run_command(ssh, install_commands["ufw"])

        # Vérifier et installer les paquets nécessaires
        for package in check_commands.keys():
            if not is_installed(ssh, package):
                print(f"Installation du paquet {package}...")
                run_command(ssh, install_commands[package])

        # Créer une connexion SFTP
        sftp = ssh.open_sftp()

        # Transférer les fichiers
        upload_files_with_structure(sftp, local_directory, remote_directory)

        # Remplacer les IP et ports dans les fichiers
        replace_ip_and_port_in_files(local_directory, domains[0], 3000, 3001)

        # Configurer chaque domaine
        for domain in domains:
            setup_domain(ssh, domain)

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Erreur lors de la configuration du VPS: {e}")

# Exécutez la fonction principale
setup_vps()
