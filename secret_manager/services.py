import base64
import os
from .models import Secret
from django.utils import timezone
from datetime import timedelta
import logging


logger = logging.getLogger(__name__)

class SecretService:
    def generate_secret(self, secret: str, passphrase: str, ttl: int) -> Secret:
        """
        Generate a new secret instance with encryption.

        Args:
            secret (str): The secret value to be stored.
            passphrase (str): The passphrase required to retrieve the secret.
            ttl (int): The time-to-live for the secret in seconds.

        Returns:
            The created Secret instance.

        Raises:
            Exception: if there is an error generating, saving the secret.
        """
        secret_instance = Secret()
        secret_instance.secret_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
        secret_instance.encrypt(secret, passphrase)
        secret_instance.ttl = timezone.now() + timedelta(seconds=int(ttl))

        self.save_secret(secret_instance)

        return secret_instance
    
    def save_secret(self, secret_instance: Secret) -> None:
        """
        Save a secret instance to the database.

        Args:
            Secret instance to save.
        
        Raises:
            Exception: if there is an error saving the secret.
        """
        try:
            secret_instance.save()
            logger.info(f"Secret saved with key: {secret_instance.secret_key}")
        except Exception as e:
            logger.error(f"Error saving secret: {e}")
            raise