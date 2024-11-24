from django.db import models
from cryptography.fernet import Fernet
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


class Secret(models.Model):
    """
    Model representing a secret.

    Attributes:
        secret_key (str): Unique key for the secret.
        encrypted_secret (bytes): The encrypted secret value.
        encrypted_passphrase (bytes): The encrypted passphrase for the secret.
        ttl (datetime): The time-to-live for the secret.
        encryption_key (str): The key used for encryption.
    """
    secret_key = models.CharField(max_length=255, unique=True)
    encrypted_secret = models.BinaryField()
    encrypted_passphrase = models.BinaryField()
    ttl = models.DateTimeField()
    encryption_key = models.CharField(max_length=255, unique=True, default='No generated key')

    def encrypt(self, secret: str, passphrase: str) -> None:
        """
        Encrypt the secret and its passphrase.

        Args:
            secret (str): The secret value to encrypt.
            passphrase (str): The passphrase to encrypt.

        Returns:
            None
        """
        self.key = Fernet.generate_key()
        f = Fernet(self.key)

        self.encrypted_secret = f.encrypt(secret.encode())
        self.encrypted_passphrase = f.encrypt(passphrase.encode())
        self.encryption_key = self.key.decode()


    def decrypt(self) -> tuple[str, str]:
        """
        Decrypt the secret and passphrase.

        Returns:
            tuple: A tuple containing the decrypted secret and passphrase.

        Raises:
            InvalidToken: If the decryption fails because of an invalid token.
        """
        f = Fernet(self.encryption_key.encode())

        decrypted_secret = f.decrypt(self.encrypted_secret.tobytes()).decode()
        decrypted_passphrase = f.decrypt(self.encrypted_passphrase.tobytes()).decode()

        return decrypted_secret, decrypted_passphrase

    
    def is_expired(self) -> bool:
        """
        Check if the secret has expired.

        Returns:
            bool: True if the secret has expired, False if not yet.
        """
        return timezone.now() > self.ttl

    def __str__(self):
        return self.secret_key
