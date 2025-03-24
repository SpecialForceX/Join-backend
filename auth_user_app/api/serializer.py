from rest_framework import serializers
from django.contrib.auth.models import User
from auth_user_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True, validators=[])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def save(self):
        password = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']

        if password != repeated_password:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        user.set_password(password)
        user.save()

        full_name = self.validated_data.get('full_name', '')
        UserProfile.objects.create(user=user, full_name=full_name)

        return user, full_name


