from  rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from urllib.parse import urljoin
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username","email","phone","auth_token",""]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email_or_username = attrs.get('username')  # Peut être un email ou un nom d'utilisateur

        # Si c'est un email, remplacer par le nom d'utilisateur
        if '@' in email_or_username:
            user = User.objects.filter(email=email_or_username).first()
            if user:
                attrs['username'] = user.username

        if email_or_username.isdigit():
            user = User.objects.filter(phone=email_or_username).first()
            if user:                
                attrs['username'] = user.username

        # Valider les données (définit self.user automatiquement)
        data = super().validate(attrs)

        # Construire l'URL de l'image
        image_url = None
        request = self.context.get("request")  # Récupérer le contexte
        if hasattr(self.user, 'image') and self.user.image and request:
            image_url = urljoin(request.build_absolute_uri('/'), self.user.image.url.lstrip('/'))

        # Ajouter des informations utilisateur supplémentaires
        data['user'] = {
            'id': self.user.id,
            'username':f"{self.user.username}",
            'email': self.user.email,
            'phone': getattr(self.user, 'phone', None),
            'full_name': f"{self.user.first_name} {self.user.last_name}",           
        }
        data['user']['groups'] = list(self.user.groups.values_list('name', flat=True))

        return data