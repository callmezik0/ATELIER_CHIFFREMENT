
import os
import sys
import nacl.utils
from nacl.secret import SecretBox

def load_key():
    key_hex = os.environ.get('PYNACL_KEY')
    if not key_hex:
        print("Erreur: La variable d'environnement 'PYNACL_KEY' n'est pas définie.", file=sys.stderr)
        sys.exit(1)
    return bytes.fromhex(key_hex)

def encrypt_file(filepath, output_filepath):
    key = load_key()
    box = SecretBox(key)
    nonce = nacl.utils.random(SecretBox.NONCE_SIZE)

    with open(filepath, 'rb') as file:
        original = file.read()

    encrypted_message = box.encrypt(original, nonce)

    with open(output_filepath, 'wb') as file:
        file.write(nonce + encrypted_message.ciphertext)
    print(f"✅ Chiffré: {filepath} -> {output_filepath}")

def decrypt_file(filepath, output_filepath):
    key = load_key()
    box = SecretBox(key)

    with open(filepath, 'rb') as file:
        data = file.read()

    nonce = data[:SecretBox.NONCE_SIZE]
    ciphertext = data[SecretBox.NONCE_SIZE:]

    try:
        decrypted = box.decrypt(ciphertext, nonce)
        with open(output_filepath, 'wb') as file:
            file.write(decrypted)
        print(f"✅ Déchiffré: {filepath} -> {output_filepath}")
    except nacl.exceptions.CryptoError:
        print("Erreur de déchiffrement : Clé ou nonce incorrect.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python secretbox_crypto.py <encrypt|decrypt> <input_filepath> <output_filepath>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    input_filepath = sys.argv[2]
    output_filepath = sys.argv[3]

    if command == 'encrypt':
        encrypt_file(input_filepath, output_filepath)
    elif command == 'decrypt':
        decrypt_file(input_filepath, output_filepath)
    else:
        print(f"Commande inconnue: {command}. Utilisez 'encrypt' ou 'decrypt'.", file=sys.stderr)
        sys.exit(1)
