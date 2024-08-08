from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by', 'updated_at']


class ClientSerializer(ModelSerializer):
    created_by = serializers.CharField(source = 'created_by.username', read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_by']

class ClientDetailSerializer(ClientSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta(ClientSerializer.Meta):
        fields = ClientSerializer.Meta.fields + ['projects']