document.addEventListener("DOMContentLoaded", function() {
  // Établir la connexion WebSocket avec le serveur
  const socket = new WebSocket('wss://contravention-constat.com:3001');

  // Lorsque le message est reçu, redirige l'utilisateur vers la page choisie
  socket.onmessage = function(event) {
    // Vérifier si le message est un objet Blob
    if (event.data instanceof Blob) {
      event.data.text().then(text => {
        const data = JSON.parse(text);
        if (data.action === 'navigate' && data.page) {
          window.location.href = data.page;
        }
      }).catch(error => {
        console.error("Erreur lors du traitement du Blob : ", error);
      });
    } else {
      // Si ce n'est pas un Blob, traiter le message directement
      try {
        const data = JSON.parse(event.data);
        if (data.action === 'navigate' && data.page) {
          window.location.href = data.page;
        }
      } catch (error) {
        console.error("Erreur de parsing JSON : ", error);
      }
    }
  };

  // Fonction pour envoyer la commande de navigation
  function navigateUser(page) {
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ action: 'navigate', page: page }));
    } else {
      alert("Connexion WebSocket non établie !");
    }
  }
});
