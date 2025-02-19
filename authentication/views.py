from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from django.db.models import Q

import re
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password  
from urllib.parse import urljoin
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # Récupérer la langue depuis les headers ou la requête
        lang = request.headers.get('language') or request.headers.get('Language') or request.META.get('HTTP_LANGUAGE')
        lang = lang if lang else "fr"


        try:

            response = super().post(request, *args, **kwargs)
            data = response.data
            data['message'] = "succes"
            return Response(data, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            # Gérer les erreurs d'authentification
            message = "erreurs d'authentification"
            return Response(
                {"error": message, "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            # Gérer les autres erreurs
            return Response(
                {"error": "Quelque chose s'est mal passée", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


        except AuthenticationFailed as e:
            if "no active account" in str(e).lower():
                message = "Idendtifiant incorrecte"
            else:
                message = "Echec d'authentification"
            return Response(
                {"error": message, "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            # Gérer les erreurs générales
            return Response(
                {"error": "Quelque chose s'est mal passee", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
class UserViewSets(viewsets.ModelViewSet):
    class_serializer = UserSerializer
    permission_classes = [IsAuthenticated]

    def logout(self, request, *args, **kwargs):
        lang = request.headers.get('language') or request.headers.get('Language') or request.META.get('HTTP_LANGUAGE')
        lang = lang if lang else "fr"
        try:
            # Récupérer le token Refresh envoyé dans le corps de la requête
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Ajouter le Refresh Token à la liste noire

            return Response({"message": "succes"}, status=200)
        except Exception as e:
            print(e)
            return Response({"error": "Echec"}, status=400)
    
    def update_password(self, request, *args, **kwargs):
        user = self.request.user
        lang = request.headers.get('language') or request.headers.get('Language') or request.META.get('HTTP_LANGUAGE')
        lang = lang if lang else "fr"
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        if not check_password(current_password, user.password):
            return Response({"error": "ancien mot de passe incorrect"}, status=400)
        if len(new_password) < 8 or not re.search(r'[A-Z]', new_password) or not re.search(r'\d', new_password) or not re.search(r'[\W_]', new_password):
            detail ="Le mot de passe doit contenir au moins 8 caractères, contenir au moins une lettre majuscule , un chiffre et un caractère spécial."
            return Response({"error": detail}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        user.set_password(new_password)
        user.save()

        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        
        # Retourner les tokens et les informations utilisateur
        response_data = {
            "refresh": str(refresh),
            "access": str(access),
            "user": {
                "id": user.id,
                'username':user.username,
                "email": user.email,
                "phone": user.phone,               
               
                "groups": list(user.groups.values_list('name', flat=True)),
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)


 
class UserSignupViewSets(viewsets.ModelViewSet):
    def signup(self, request, *args, **kwargs):
        lang = request.headers.get('language') or request.headers.get('Language') or request.META.get('HTTP_LANGUAGE')
        lang = lang if lang else "fr"
        # try:
        username = request.data.get('username', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email = request.data.get('email', '')
        phone = request.data.get('phone', '')
        password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')
        
        
        group, created = Group.objects.get_or_create(name='customers')
        user = User.objects.create(
            username=username,
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )
        group.user_set.add(user)
        user.set_password(password)
        user.save()

        # Générer les tokens
        token_data = {'username':f"{user.username}", "password": password}
        serializer = CustomTokenObtainPairSerializer(data=token_data)
        serializer.is_valid(raise_exception=True)

       
        response_data = {
            "refresh": serializer.validated_data["refresh"],
            "access": serializer.validated_data["access"],
            "user": {
                "id": user.id,
                'username':user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name":user.last_name,                
                "groups": list(user.groups.values_list('name', flat=True)),
            },
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

        