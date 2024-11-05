<?php
// Détecter la langue de l'utilisateur
$lang = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2);

// Définir les traductions
$translations = [
    'en' => [
        'title' => 'Document'
    ],
    'fr' => [
        'title' => 'Document en Français'
    ]
];

// Sélectionner la traduction appropriée
$selected_lang = $translations[$lang] ?? $translations['en'];
?>

<!DOCTYPE html>
<html lang="<?php echo $lang; ?>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $selected_lang['title']; ?></title>
</head>
<body>

    <script src="js/controle.js"></script>
  
</body>
</html>
