from rest_framework import serializers
from django.contrib.auth.models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','password2']
        
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('PassWords Do Not Match.')
            
        return data
        
    def create(self,validated_data):
        validated_data.pop('password2')
            
        user_obj = User.objects.create_user(
                username = validated_data['username'],
                email = validated_data['email'],
                password = validated_data['password']
            )
            
        return user_obj
    