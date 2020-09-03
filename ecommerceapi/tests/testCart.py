import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Test