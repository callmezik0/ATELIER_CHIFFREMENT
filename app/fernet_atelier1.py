
import os
import sys
from cryptography.fernet import Fernet

def load_key():
    key = os.environ.get('FERNET_KEY')
    if not key:
        print("Erreur: La variable d'environnement 'FERNET_KEY' n'est pas définie.", file=sys.stderr)
        sys.exit(1)
    return key.encode('utf-8')

def encrypt_file(filepath, output_filepath):
    key = load_key()
    f = Fernet(key)
    with open(filepath, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(output_filepath, 'wb') as file:
        file.write(encrypted)
    print(f"✅ Chiffré: {filepath} -> {output_filepath}")

def decrypt_file(filepath, output_filepath):
    key = load_key()
    f = Fernet(key)
    with open(filepath, 'rb') as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    with open(output_filepath, 'wb') as file:
        file.write(decrypted)
    print(f"✅ Déchiffré: {filepath} -> {output_filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python fernet_atelier1.py <encrypt|decrypt> <input_filepath> <output_filepath>", file=sys.stderr)
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
