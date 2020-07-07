import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from cards.models import Cardset
from backend import settings
from .serializers import UserSerializer, GroupSerializer, UserGetSerializer

# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserGetSerializer

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def return_cards(self, request, pk=None):
        user = self.get_object()
        cardsets = Cardset.objects.filter(owner=user)


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        user["password"] = make_password(user["password"])
        serializer_context = {
            "request": request
        }
        serializer = UserSerializer(data=user,context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer_context = {
            "request": request
        }
        serializer = self.serializer_class(request.user, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer_context = {
            "request": request
        }
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny,])
def authenticate_user(request):

    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email)
        if user and check_password(password, user.password):
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error' : "please provide an email and password" }
        return Response(res)


