from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import SecretService
from .models import Secret
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)

class GenerateSecretView(APIView):
    def post(self, request) -> Response:
        """
        Handle POST requests, generate a new secret.

        Args:
            HTTP request object containing the secret data.

        Returns:
            A Response object containing the generated secret key or an error message.

        Raises:
            ValueError: If the secret or passphrase is not provided.
            Exception: If an error occurs while generating the secret.
        """
        secret = request.data.get('secret')
        passphrase = request.data.get('passphrase')
        ttl = request.data.get('ttl')

        if not secret or not passphrase:
            logger.warning("Secret and passphrase are required.")
            return Response({"error": "Secret and passphrase are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            secret_instance = SecretService().generate_secret(secret, passphrase, ttl)
            return Response({"secret_key": secret_instance.secret_key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error generating secret: {e}")
            return Response({"error": "An error occurred while generating the secret."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrieveSecretView(APIView):
    def get(self, request, secret_key: str) -> Response:
        """
        Retrieve a secret using the secret key and passphrase.

        Args:
            The HTTP request object.
            secret_key (str): The key of the secret to retrieve.

        Returns:
            Response object containing the secret or an error message.

        Raises:
            ValueError: If the secret key is not provided.
            Secret.DoesNotExist: If the secret is not found in the database.
            Exception: For general errors during retrieval.
        """
        passphrase = request.query_params.get('passphrase')

        if not secret_key:
            return Response({"error": "Secret key is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            secret_instance = Secret.objects.get(secret_key=secret_key)
        except Secret.DoesNotExist:
            return Response({"error": "Secret not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Database error while retrieving secret: {e}")
            return Response({"error": "General error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if timezone.now() > secret_instance.ttl:
            secret_instance.delete()
            logger.warning(f"Secret has expired for key {secret_key}")
            return Response({"error": "Secret has expired."}, status=status.HTTP_410_GONE)
            
        decrypted_secret, decrypted_passphrase = secret_instance.decrypt()

        if passphrase != decrypted_passphrase:
            logger.warning("Invalid passphrase provided.")
            return Response({"error": "Invalid passphrase."}, status=status.HTTP_403_FORBIDDEN)
            
        logger.info(f"Received secret_key: {secret_key}")
        return Response({"secret": decrypted_secret}, status=status.HTTP_200_OK)
