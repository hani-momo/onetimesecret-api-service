from django.urls import path
from .views import GenerateSecretView, RetrieveSecretView


urlpatterns = [
    path('generate/', GenerateSecretView.as_view(), name='generate_secret'),
    path('secrets/<str:secret_key>/', RetrieveSecretView.as_view(), name='retrieve_secret'),
]
