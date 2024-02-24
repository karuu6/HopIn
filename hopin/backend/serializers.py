from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required = True, write_only = True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

