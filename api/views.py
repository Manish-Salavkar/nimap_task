from .serializers import ClientSerializer, ProjectSerializer, ClientDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Client, Project
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# ----------------------------------------------------------------------------------
# Client CRUD Operations

class ClientViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        client_projects = Project.objects.filter(client=instance)
        project_data = ProjectSerializer(client_projects, many=True).data

        data['projects'] = project_data

        return Response(data, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)

# ----------------------------------------------------------------------------------
# Project Operations

class CreateProject(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        project_name = request.data.get('project_name', '')
        users_data = request.data.get('users', [])
        client_id = id
        user_id = request.user.id

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        project_data = {
            'project_name': project_name,
            'client': client.id,
            'created_by': user_id,
        }

        project_serializer = ProjectSerializer(data=project_data)

        if project_serializer.is_valid():
            project = project_serializer.save()

            for user_data in users_data:
                user_id = user_data.get('id')
                name = user_data.get('name')
                try:
                    user = User.objects.get(id=user_id, username=name)
                    project.users.add(user)
                except User.DoesNotExist:
                    return Response({'error': f'User with id {user_id} and name {name} not found'}, status=status.HTTP_400_BAD_REQUEST)
           
            response_data = ProjectSerializer(project).data
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------
# List User assigned Projects

class ListUserProjects(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        projects = Project.objects.filter(users=user)
        serializer = ProjectSerializer(projects, many=True)

        response_data = [
            {
                'id': project.id,
                'project_name': project.project_name,
                'created_at': project.created_at.isoformat(),
                'created_by': project.created_by.username,
            }
            for project in projects
        ]
        return Response(response_data, status=status.HTTP_200_OK)