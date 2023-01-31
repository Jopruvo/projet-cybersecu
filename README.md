Projet d'INFO731 avec TAKAHASHI &amp; GONAY &amp; OUKZIZ &amp; BOUGHAMNI &amp; Moi-même
liens utile : https://pycryptodome.readthedocs.io/en/latest/src/installation.html

# Projet de Proxy de sécurité Web

## Objectif

Le but de ce projet est de développer un proxy de sécurité pour la communication web en mettant en place un mécanisme qui permet de chiffrer le traffic à l'entrée d'un domaine où le traffic est susceptible d'être écouté et de déchiffrer celui-ci à la sortie.

## Fonctionnalités

- Construction d'un proxy acceptant les requêtes web et les renvoyant vers un proxy de sortie qui fait la requête à leur place
- Implantation d'un mécanisme d'échange de clé d'encryption par clé publique avec utilisation de la librairie de cryptographie RSA
- Utilisation de la clé d'encryption échangée par le mécanisme RSA pour chiffrer le traffic

## Processus

1. Le proxy reçoit les requêtes HTTP d'un navigateur web configuré pour utiliser un proxy
2. Le proxy chiffre ces requêtes avant de les envoyer au proxy de sortie
3. Le proxy de sortie fait la requête HTTP au serveur web à la place du navigateur web
4. Le proxy de sortie reçoit la réponse, la chiffre et la renvoie vers le proxy source
5. Le proxy source renvoie finalement la réponse au navigateur qui affiche la page demandée.

## Fonctions de browser_handler:

- `find_free_port` : trouver un port libre pour le serveur proxy.
- `init_sock` : initialiser les sockets du serveur proxy.
- `send_request` : envoyer la requête cryptée au serveur. Elle génère d'abord des clés publique et privée RSA, puis envoie la clé publique RSA au destinataire (le serveur). Ensuite, elle reçoit la clé publique du serveur, puis envoie la requête cryptée.
- `receive_response` : recevoir la réponse cryptée du serveur. Elle déchiffre la réponse et la renvoie au client.
- `start` : fonction principale qui initialise le socket, écoute sur le port 8080 et démarre un nouveau thread pour chaque requête reçue. Le serveur est en mode de boucle infinie pour continuer à écouter les requêtes entrantes.

Ce code représente un serveur proxy qui écoute sur le port `8080` et envoie des requêtes sur le port `8081`. Il utilise le protocole RSA pour chiffrer les requêtes et les réponses envoyées entre le client et le serveur.

En cas d'interruption du clavier, le serveur est fermé et le message "Proxy server Shutting Down" est affiché à l'écran.

## Fonction de serveur_handler

Ce code est un serveur proxy qui permet à un client de faire des requêtes HTTP ou HTTPS en passant par un serveur proxy. Il utilise :

- Le module `_thread` pour gérer les connexions clientes de manière asynchrone
- Le module `socket` pour gérer les connexions réseau
- Le module `Cryptodome.PublicKey` pour gérer les clés publiques RSA
- La fonction `encrypt_message` et `decrypt_message` du module `rsa_fct` pour chiffrer et déchiffrer les messages RSA

## Variables

- `listening_port` définit le numéro de port sur lequel le serveur proxy écoutera les connexions clientes
- `max_conn` définit le nombre maximum de connexions simultanées que le serveur proxy peut gérer
- `buffer_size` définit la taille du buffer pour les données reçues ou envoyées
- `client_public_key_rsa_key` est utilisée pour stocker la clé publique RSA du client

## Fonctions

- `proxy_server` est appelée lorsqu'une connexion client est établie. Elle analyse la première ligne de la demande client pour déterminer si c'est une requête HTTP ou HTTPS. Si c'est une requête HTTPS, elle appelle la fonction `https_request`, sinon elle appelle la fonction `http_request`.

- `https_request` crée une nouvelle connexion socket vers le serveur web cible et envoie une réponse 200 code pour indiquer que la connexion est établie. Ensuite, il écoute et transfère les données entre la connexion client et le serveur web cible.

- `http_request` crée une nouvelle connexion socket vers le serveur web cible et envoie la demande client. Ensuite, il écoute les réponses du serveur web cible et les transfère à la connexion client.

- `conn_string` analyse la demande client pour extraire les informations sur le serveur web cible et le port. Il appelle la fonction `proxy_server` pour gérer la demande client.

- `reciev_request` est appelée pour écouter les connexions clientes et appelle la fonction `conn_string` pour gérer chaque demande client.

## Conclusion

Ce code implémente un serveur proxy qui permet aux clients de faire des requêtes HTTP et HTTPS en passant par un serveur proxy. Les connexions clientes sont gérées de manière asynchrone et les demandes sont transmises au serveur web cible en utilisant des sockets.


