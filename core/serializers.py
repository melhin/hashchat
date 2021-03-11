from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import User
from core.choices import LanguageChoices


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField()
    company = serializers.CharField(max_length=50)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LanguageSelectorSerializer(serializers.Serializer):
    language_code = serializers.ChoiceField(
        choices=[(lang, lang.value) for lang in LanguageChoices],
    )

    class Meta:
        fields = [
            'language_code'
        ]
