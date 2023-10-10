from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from TankSaverAPI import models
from .api.serializer import CompraSerializer, PostoSerializer
from django.http import Http404

     
