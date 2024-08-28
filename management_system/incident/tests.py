from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()
try:
    user = User.objects.get(email="imvibhuti364@gmail.com")
    print(f"User: {user.username}, Email: {user.email}")
except ObjectDoesNotExist:
    print("User does not exist.")
