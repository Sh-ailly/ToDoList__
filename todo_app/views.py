from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import todomodel
from .serializers import TodoSerializer

# Create your views here.
class TodoViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

     #Custom method to handle pagination
    def paginate_queryset(self, queryset, request):
        page_size = 2  # Number of items per page
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size
        return queryset[start:end]
    # GET
    def list(self, request):
        completed = request.query_params.get('completed', None)
        title = request.query_params.get('title', None)

        todos = todomodel.objects.filter(user=request.user)

        if completed is not None:
            if completed.lower()=='true':
                todos=todos.filter(completed=True)
            elif completed.lower()=='false':
                todos=todos.filter(completed=False)

        if title:
            todos = todos.filter(title__icontains=title)

        paginated_todos = self.paginate_queryset(todos, request)

        serializer = TodoSerializer(paginated_todos, many=True)
        return Response(serializer.data)

    # POST
    def create(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET
    def retrieve(self, request, pk=None):
        try:
            todo = todomodel.objects.get(pk=pk, user=request.user)
        except todomodel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    # PUT
    def update(self, request, pk=None):
        try:
            todo = todomodel.objects.get(pk=pk, user=request.user)
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
            todo = todomodel.objects.get(pk=pk, user=request.user)
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
            todo = todomodel.objects.get(pk=pk, user=request.user)
        except todomodel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
