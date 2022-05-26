from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and ""confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
    )
        user_list = User.objects.all()
        group = Group.objects.all()
        group.user_set.add(*user_list)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'email',
            'groups',
        )