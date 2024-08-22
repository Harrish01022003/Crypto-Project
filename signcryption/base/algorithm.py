from Crypto.PublicKey import ECC
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import os

def generate_key_pair():
    key = ECC.generate(curve='P-256')
    private_key = key.export_key(format='PEM')
    public_key = key.public_key().export_key(format='PEM')
    return private_key, public_key

def save_key_to_file(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)

def load_key_from_file(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key

def encrypt_file(public_key_file, input_file, output_file):
    public_key = ECC.import_key(load_key_from_file(public_key_file))


    aes_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_aes_key = cipher_rsa.encrypt(aes_key)

    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)


    with open(output_file, 'wb') as f:
        for x in (enc_aes_key, cipher_aes.nonce, tag, ciphertext):
            f.write(x)

def decrypt_file(private_key_file, input_file, output_file):
    private_key = ECC.import_key(load_key_from_file(private_key_file))


    with open(input_file, 'rb') as f:
        enc_aes_key, nonce, tag, ciphertext = [f.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]


    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(enc_aes_key)


    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag)

    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Example usage:
private_key, public_key = generate_key_pair()
save_key_to_file(private_key, 'private_key.pem')
save_key_to_file(public_key, 'public_key.pem')

encrypt_file('public_key.pem', 'input.txt', 'encrypted_file.bin')
decrypt_file('private_key.pem', 'encrypted_file.bin', 'decrypted_file.txt')
