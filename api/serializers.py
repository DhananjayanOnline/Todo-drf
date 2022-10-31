
from rest_framework import serializers

from api.models import Todo
from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Todo
        fields = ['id', 'task_name','user', 'status']
    
    def create(self, validated_data):
        user = self.context.get('user')
        return Todo.objects.create(**validated_data, user=user)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)