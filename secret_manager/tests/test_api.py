from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import time


class SecretAPITests(APITestCase):

    def test_generate_secret(self):
        response = self.client.post(reverse('generate_secret'), {
            'secret': 'test_secret', 
            'passphrase': 'test_passphrase', 
            'ttl': 60
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('secret_key', response.data)

    def test_retrieve_secret_with_valid_inputs(self):
        response = self.client.post(reverse('generate_secret'), {
            'secret': 'test_secret', 
            'passphrase': 'test_passphrase', 
            'ttl': 60
        })
        secret_key = response.data.get('secret_key')

        response = self.client.get(reverse('retrieve_secret', args=[secret_key]), {
            'passphrase': 'test_passphrase'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('secret', response.data)
        self.assertEqual(response.data['secret'], 'test_secret')
    
    def test_retrieve_expired_secret(self):
        response = self.client.post(reverse('generate_secret'), {
            'secret': 'test_secret', 
            'passphrase': 'test_passphrase', 
            'ttl': 1
        })
        secret_key = response.data.get('secret_key')

        time.sleep(2)

        response = self.client.get(reverse('retrieve_secret', args=[secret_key]), {
            'passphrase': 'test_passphrase'
        })
        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertEqual(response.data, {"error": "Secret has expired."})

    def test_retieve_non_existent_secret(self):
        response = self.client.get(reverse('retrieve_secret', args=['non_existent_key']), {
            'passphrase': 'test_passphrase'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Secret not found."})
    
    def test_retrieve_secret_with_invalid_passphrase(self):
        response = self.client.post(reverse('generate_secret'), {
            'secret': 'test_secret', 
            'passphrase': 'test_passphrase', 
            'ttl': 60
        })
        secret_key = response.data.get('secret_key')

        response = self.client.get(reverse('retrieve_secret', args=[secret_key]), {
            'passphrase': 'wrong_passphrase'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "Invalid passphrase."})
