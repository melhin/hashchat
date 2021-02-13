from rest_framework import serializers
from core.models import User
from rest_framework.validators import UniqueValidator
    

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField()
    company = serializers.CharField(max_length=50)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
