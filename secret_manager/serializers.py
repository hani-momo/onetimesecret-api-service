from rest_framework import serializers
from .models import Secret


class SecretSerializer(serializers.ModelSerializer):
    """
    Serializer for the Secret Model,
    handles the serialization and deserialization of Secret instances.
    """
    class Meta:
        model = Secret
        fields = ['secret_key', 'encrypted_passphrase', 'encrypted_secret', 'ttl']
