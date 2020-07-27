from PIL import Image
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from cards.models import Cardset, Language
from .filters import ProfileFilter
from .models import Profile
from .permissions import IsReadOnlyOrIsOwner
from .schemas import *
from .serializers import GroupSerializer, UserGetSerializer, ProfileSerializer, ProfileSerializerDetail, \
    PhotosProfileSerializer, ProfileEditSerializerDetail

# Create your views here.

API_URL = "http://localhost:8000/docs"
WRONG_JSON_ERROR = _("Wrong JSON. Please read API documentation: ") + API_URL




class FriendsListAPI (ListAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if (user):
            queryset = user.profile.get_friends()
            return queryset
        return None


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to get full user infomation
    """
    queryset = Profile.objects.all().order_by('user__last_login')
    permission_classes = [IsReadOnlyOrIsOwner, IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'toggle_follow':
            return ProfileSerializer
        elif self.action == 'change_avatar':
            return PhotosProfileSerializer
        elif self.action == 'create' or self.action == 'update':
            return ProfileEditSerializerDetail
        return ProfileSerializerDetail


    def retrieve(self, request, pk=None):
        user = User.objects.get(id=pk)
        if user:
            profile = Profile.objects.get(user=user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            res = {
                "message": _("No existing user with that ID")
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        profile = Profile.objects.get(user_id=pk)
        if profile:
            try:
                data = self.get_serializer(data=request.data)
                data.is_valid()
                profile.hobbies = data.validated_data["hobbies"]
                profile.about_me = data.validated_data["about_me"]
                profile.birth_date = data.validated_data["birth_date"]
                languages_know = Language.objects.filter(name__in=request.data['languages_know'])
                languages_learn = Language.objects.filter(name__in=request.data['languages_learn'])
                profile.languages_know.set(languages_know)
                profile.languages_learn.set(languages_learn)
                profile.save()
            except KeyError as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        res = {
            "message": _("No existing user with that ID")
        }
        return Response(res, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True,
            url_path='follow',
            url_name='toggle_follow',
            methods=['post', 'delete'],
            schema=toggle_follow_schema,
            permission_classes=[IsReadOnlyOrIsOwner, IsAuthenticated]
            )
    def toggle_follow(self, request, pk=None):
        try:
            me = request.user
            user = User.objects.get(id=pk)
            serializer = self.get_serializer(user.profile)
            if request.method == 'POST':
                me.profile.add_following(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif request.method == 'DELETE':
                me.profile.delete_following(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message" : "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            url_path='language',
            url_name='set_language',
            methods=['post'],
            schema=profile_languages_schema,
            permission_classes=[IsReadOnlyOrIsOwner, IsAuthenticated])
    def set_language(self, request):
        """
        Endpoint to delete or add language of current user.

        * Required JWT authentification

        """
        try:
            user = request.user
            languages = Language.objects.filter(name__in=request.data['languages'])
            field_name = request.data['field']
            if request.data['action'] == 'ADD':
                try:
                    if field_name == 'language_know':
                        user.profile.languages_know.add(*languages)
                    elif field_name == 'language_learn':
                        user.profile.languages_learn.add(*languages)
                    else:
                        error = {
                            'field': _("Wrong field name. Only 'language_know' and 'language_learn' are possible.")
                        }
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    raise e
                user.save()
                return Response(request.data, status=status.HTTP_201_CREATED)
            elif request.data['action'] == 'DELETE':
                try:
                    if field_name == 'language_know':
                        user.profile.languages_know.remove(*languages)
                    elif field_name == 'language_learn':
                        user.profile.languages_learn.remove(*languages)
                    else:
                        error = {
                            'field': _("Wrong field name. Only 'language_know' and 'language_learn' are possible.")
                        }
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                user.save()
                return Response(request.data, status=status.HTTP_204_NO_CONTENT)
            else:
                error = {
                    'action': _("Wrong action. Only actions DELETE and ADD are available.")
                }


        except KeyError:
            error = {
                'message': _('Wrong JSON. Please read API on how to use this endpoint: ')
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            url_path='hobbies',
            url_name='change_hobbies',
            methods=['put'],
            schema=change_hobbies_schema,
            permission_classes=[IsReadOnlyOrIsOwner, IsAuthenticated])
    def change_hobbies(self, request):
        try:
            user = request.user
            user.profile.hobbies = request.data['hobbies']
            user.profile.save()
        except KeyError:
            error = {
                "message": WRONG_JSON_ERROR
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)

    @action(detail=False,
            url_path='about',
            url_name='change_about',
            methods=['put'],
            schema=change_about_schema,
            permission_classes=[IsReadOnlyOrIsOwner, IsAuthenticated])
    def change_about(self, request):
        try:
            user = request.user
            user.profile.about_me = request.data['about']
            user.profile.save()
        except KeyError:
            error = {
                "message": WRONG_JSON_ERROR
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


    @action(detail=False,
            url_path='avatar',
            url_name='change_avatar',
            methods=['put', 'delete'],
            schema=change_avatar_schema,
            permission_classes=[IsReadOnlyOrIsOwner, IsAuthenticated],
            parser_classes=[MultiPartParser, FormParser]
            )
    def change_avatar(self, request, format=None):
        user = request.user
        if request.method == "DELETE":
            user.profile.avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if 'file' not in request.data:
            raise ParseError("Empty content")
        file = request.data['file']
        try:
            print("Before open")
            img = Image.open(file)
            print("After open")
            img.verify()
            print("After verify")

        except:
            raise ParseError("Unsupported image type")
        user.profile.avatar.delete(save=True)
        user.profile.avatar.save(file.name, file, save=True)

        serializer = self.get_serializer(user.profile)
        # data = {
        #     "photos": {
        #         "avatar" : user.profile.avatar.url,
        #         "avatar_small" : user.profile.avatar_small.url,
        #         "avatar_medium" : user.profile.avatar_medium.url,
        #         "avatar_big" : user.profile.avatar_big.url,
        #     }
        # }
        return Response(serializer.data, status=status.HTTP_201_CREATED)



#@api_view(['POST'])
#@permission_classes([IsReadOnlyOrIsOwner, IsAuthenticated])
#@schema(profile_languages_schema)








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


# class CreateUserAPIView(APIView):
#     # Allow any user (authenticated or not) to access this url
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         user = request.data
#         user["password"] = make_password(user["password"])
#         serializer_context = {
#             "request": request
#         }
#         serializer = UserSerializer(data=user,context=serializer_context)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         Profile.objects.all().create(user=User.objects.get(username=user["username"]))
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     # Allow only authenticated users to access this url
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
#
#
#     def get(self, request, *args, **kwargs):
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         serializer_context = {
#             "request": request
#         }
#         serializer = self.serializer_class(request.user, context=serializer_context)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#         serializer_context = {
#             "request": request
#         }
#         serializer = UserSerializer(
#             request.user, data=serializer_data, partial=True, context=serializer_context
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny,])
# def authenticate_user(request):
#
#     try:
#         email = request.data['email']
#         password = request.data['password']
#
#         user = User.objects.get(email=email)
#         if user and check_password(password, user.password):
#             try:
#                 payload = jwt_payload_handler(user)
#                 token = jwt.encode(payload, settings.SECRET_KEY)
#                 user_details = {'id': user.id, 'email': email, 'login': user.username, 'token': token}
#                 user_logged_in.send(sender=user.__class__, request=request, user=user)
#                 return Response(user_details, status=status.HTTP_200_OK)
#             except Exception as e:
#                 raise e
#         else:
#             res = {
#                 'error': _('Can not authenticate with given credentials or the account has been deactivated')
#             }
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {'error' : _("Please provide an email and password") }
#         return Response(res)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):

    """
    Blacklist requested refresh token. Use to unlogin users.
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)