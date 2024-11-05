// Installation : npm install ws https
import { Server, OPEN } from 'ws';
import { createServer } from 'https';
import { readFileSync } from 'fs';

// Charger le certificat et la clé
const server = createServer({
  cert: readFileSync('/etc/letsencrypt/live/contravention-constat.com/fullchain.pem'),
  key: readFileSync('/etc/letsencrypt/live/contravention-constat.com/privkey.pem')
});

const wss = new Server({ server });

wss.on('connection', ws => {
  ws.on('message', message => {
    // Broadcast le message à tous les utilisateurs connectés
    wss.clients.forEach(client => {
      if (client.readyState === OPEN) {
        client.send(message);
      }
    });
  });
});

server.listen(3001, () => {
  console.log('Serveur WebSocket en écoute sur wss://contravention-constat.com:3001');
});
