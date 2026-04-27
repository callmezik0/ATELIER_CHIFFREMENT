# Atelier – Chiffrement/Déchiffrement (Python `cryptography`) dans GitHub Codespaces

## 1) Lancer le projet dans Codespaces
- Fork / clone ce repo
- Bouton **Code** → **Create codespace on main**

## 2) Installer la bibliothèque Python Cryptographie
```bash
pip install -r requirements.txt
```
## 3) Partie A – Chiffrer/Déchiffrer un texte
```
python app/fernet_demo.py
```
**Quel est le rôle de la clé Fernet ?**  
La clé Fernet est une clé symétrique secrète de 256 bits encodée en Base64, utilisée pour chiffrer et authentifier les données avec AES et HMAC issue de la bibliothèque python cryptography. Un token Fernet (c'est à dire le résultat chiffré) contient :  
```
| Version | Timestamp | IV | Ciphertext | HMAC |
```
* Version (1 octet) : Valeur actuelle : 0x80
* Timestamp (8 octets) : Permet l'expiration des tokens
* IV (16 octets) : Généré aléatoirement - Garantit que deux messages identiques produisent des ciphertexts différents
* Ciphertext (variable) : Résultat du chiffrement AES-128-CBC qui contient les données
* HMAC (32 octets) : Protège contre toute modification
  
## 4) Partie B – Chiffrer/Déchiffrer un fichier
Créer un fichier de test :  
```
echo "Message Top secret !" > secret.txt
```
Chiffrer :
```
python app/file_crypto.py encrypt secret.txt secret.enc
```
Déchiffrer :
```
python app/file_crypto.py decrypt secret.enc secret.dec.txt
cat secret.dec.txt
```
**Que se passe-t-il si on modifie un octet du fichier chiffré ?**  
 
**Pourquoi ne faut-il pas commiter la clé dans Git ?**   

## 5) Atelier 1 :
Dans cet atelier, la clé Fernet n'est plus générée dans le code mais stockée dans un Repository Secret Github. Ecrivez un nouveau programme **python app/fernet_atelier1.py** qui utilisera une clé Fernet caché dans un Secret GitHub pour encoder et décoder vos fichiers.

## 6) Atelier 2 :
Les bibliothèques qui proposent un système complet, sûr par défaut et simple d’usage comme Fernet de la bibliothèse Cryptographie sont relativement rares. Toutefois, la bibliothèque PyNaCl via l'outil SecretBox est une très bonne alternative. **travail demandé :** Construire une solution de chiffrement/déchiffrement basé sur l'outils SecretBox de la bibliothèque PyNaCl.











## Réponses aux Questions


### Question 1: Que se passe-t-il si on modifie un octet du fichier chiffré ?
**Réponse:** Si un octet du fichier chiffré par Fernet est modifié, le processus de déchiffrement échouera. Fernet inclut un HMAC (Hash-based Message Authentication Code) dans le token chiffré. Ce HMAC est calculé sur les données chiffrées (y compris l'IV et le texte chiffré). Lors du déchiffrement, le HMAC est recalculé et comparé à celui inclus dans le token. Si un seul octet des données chiffrées est altéré, les HMAC ne correspondront pas, indiquant une altération du message. Cela déclenchera une erreur `cryptography.fernet.InvalidToken` ou similaire, protégeant ainsi l'intégrité des données et empêchant le déchiffrement de données corrompues ou falsifiées.

### Question 2: Pourquoi ne faut-il pas commiter la clé dans Git ?
**Réponse:** Il ne faut jamais commiter de clés de chiffrement (ou toute autre information sensible comme des mots de passe, des API keys, etc.) dans un dépôt Git pour plusieurs raisons critiques :
1.  **Sécurité**: Une fois une clé poussée sur un dépôt (surtout public), elle est potentiellement accessible à quiconque ayant accès au dépôt, compromettant la sécurité des données chiffrées avec cette clé. Même si la clé est retirée ultérieurement de l'historique visible, elle peut toujours exister dans l'historique du dépôt.
2.  **Rotation des Clés**: Les clés doivent être régulièrement renouvelées (rotées). Si une clé est "hardcodée" et versionnée, la rotation devient difficile et risque de casser des applications dépendantes de cette clé.
3.  **Environnements Multiples**: Différents environnements (développement, test, production) devraient utiliser des clés distinctes. Commiter une clé force son utilisation dans tous les environnements, augmentant le risque de compromission générale.
4.  **Conformité**: De nombreuses normes de sécurité et réglementations (ex: GDPR, HIPAA) exigent que les clés de chiffrement soient gérées de manière sécurisée et ne soient pas exposées dans le code source.

Les clés doivent être gérées via des mécanismes sécurisés comme les variables d'environnement, les secrets managers (Vault, AWS Secrets Manager, Google Secret Manager), ou des fichiers de configuration spécifiques non versionnés (.env).
