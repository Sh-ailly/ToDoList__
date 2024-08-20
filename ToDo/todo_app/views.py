from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import todomodel
from .serializers import TodoSerializer

# Create your views here.
class TodoViewSet(viewsets.ViewSet):
    # GET
    def list(self, request):
        queryset = todomodel.objects.all()
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data)

    # POST
    def create(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET
    def retrieve(self, request, pk=None):
        try:
            todo = todomodel.objects.get(pk=pk)
        except todomodel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    # PUT
    def update(self, request, pk=None):
        try:
            todo = todomodel.objects.get(pk=pk)
        except todomodel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH
    def partial_update(self, request, pk=None):
        try:
            todo = todomodel.objects.get(pk=pk)
        except todomodel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def destroy(self, request, pk=None):
        try:
            todo = todomodel.objects.get(pk=pk)
        except todomodel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
