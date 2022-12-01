
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from api.models import Todo
from django.contrib.auth.models import User
from api.serializers import TodoSerializer, RegistrationSerializer
from rest_framework import authentication, permissions

from rest_framework.decorators import action

# Create your views here.



class TodoView(ViewSet):
    def list(self, request, *args, **kwargs):
        qs = Todo.objects.all()
        serializer = TodoSerializer(qs, many=True)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        qs = Todo.objects.get(id=id)
        serializer = TodoSerializer(qs)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        Todo.objects.get(id=id).delete()
        return Response(data='deleted')

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        qs = Todo.objects.get(id=id)
        serializer = TodoSerializer(data=request.data, instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

from .custompermission import IsOwnerPermission

class TodosModelViews(ModelViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[IsOwnerPermission]

    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

    # def list(self, request, *args, **kwargs):
    #     user=request.user
    #     qs= Todo.objects.filter(user=user)
    #     serializer = TodoSerializer(qs, many=True)
    #     return Response(data=serializer.data)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todo.objects.create(**serializer.validated_data, user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer= TodoSerializer(data=request.data, context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            serializer.errors

    @action(methods=["GET"], detail=False)
    def pending_todos(self, request, *args, **kwargs):
        pending = Todo.objects.filter(status=False, user=request.user)
        serializer = TodoSerializer(pending, many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"], detail=False)
    def completed_todos(self, request, *args, **kwargs):
        completed = Todo.objects.filter(status=True)
        serializer = TodoSerializer(completed, many=True)
        return Response(data=serializer.data)

    @action(methods=['POST'], detail=True)
    def mark_as_done(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        item = Todo.objects.get(id=id)
        item.status = True
        item.save()
        serializer = TodoSerializer(item, many=False)
        return Response(data='updated')

    
class UsersView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serialaizer= RegistrationSerializer(data=request.data)
    #     if serialaizer.is_valid():
    #         User.objects.create_user(**serialaizer.validated_data)
    #         return Response(data=serialaizer.data)
    #     else:
    #         return Response(data=serialaizer.errors)