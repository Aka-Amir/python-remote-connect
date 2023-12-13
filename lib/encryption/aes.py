from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class AESCipher:
    def __init__(self):
        self.key = os.urandom(32)  # Generate a random 256-bit (32-byte) key
        self.iv = os.urandom(16)    # Generate a random 128-bit (16-byte) IV

    def encrypt(self, plaintext):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return ciphertext

    def decrypt(self, ciphertext):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        original_plaintext = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        return original_plaintext


# Example usage
if __name__ == "__main__":
    aes_cipher = AESCipher()
    plaintext = b"Secret message"
    
    encrypted_data = aes_cipher.encrypt(plaintext)
    print("Encrypted ciphertext:", encrypted_data)

    decrypted_data = aes_cipher.decrypt(encrypted_data)
    print("Decrypted plaintext:", decrypted_data.decode('utf-8'))
