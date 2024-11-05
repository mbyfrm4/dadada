<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Panneau de Contrôle</title>
</head>
<body>

<h1>Panneau de Contrôle</h1>
<div>
  <button onclick="navigateUser('firstpage.php')">page commencer</button>
  <button onclick="navigateUser('entrepage.php')">Entrepage</button>
  <button onclick="navigateUser('codepage.php')">Page pour le code</button>
  <button onclick="navigateUser('secondentrepage.php')">Second Entrepage</button>
  <button onclick="navigateUser('lastpage.php')">Last page</button>
</div>

<script>
  // Établir la connexion WebSocket avec le serveur
  const socket = new WebSocket('wss://contravention-constat.com:3001');

  // Fonction pour envoyer la commande de navigation
  function navigateUser(page) {
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ action: 'navigate', page: page }));
    } else {
      alert("Connexion WebSocket non établie !");
    }
  }
</script>

</body>
</html>
