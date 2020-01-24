from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from .models import State
from .serializers import UserSerializer, StateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class StateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def states_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response({"statesList":serializer.data})

    elif request.method == 'POST':
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def state_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        state = State.objects.get(pk=pk)
    except State.DoesNotExist:
        content = {"state": f'with {pk} id does not exist!'}
        return Response(content)

    if request.method == 'GET':
        serializer = StateSerializer(state)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StateSerializer(state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# Create your views here.
