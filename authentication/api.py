from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.views import LoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import viewsets,status
from authentication.serializers import LqProfileSerializer,LqUserSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from authentication.models import LqProfile,LqUser
from rest_framework.response import Response
from rest_framework.decorators import list_route,detail_route
# from rest_auth.views import  LoginView as login_view
from django.conf import settings



# class LoginView(login_view):
#     def get_response(self):
#         serializer_class = self.get_response_serializer()
#
#         if getattr(settings, 'REST_USE_JWT', False):
#             data = {
#                 'user': self.user,
#                 'token': self.token
#             }
#             serializer = serializer_class(instance=data,
#                                           context={'request': self.request})
#         else:
#             serializer = serializer_class(instance=self.token,
#                                           context={'request': self.request})
#         print("Override view called")
#         return Response(serializer.data, status=status.HTTP_200_OK)

class CheckAuth(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=["get"])
    def check_auth(self,request):
        try:
            user = LqUser.objects.get(pk=request.user.id)
            serializer = LqUserSerializer(user)
            return Response(serializer.data)
        except:
            return Response({})


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class UserRegistraionViewset(viewsets.ModelViewSet):
    serializer_class = LqProfileSerializer
    permission_classes =(permissions.IsAuthenticatedOrReadOnly,)
    queryset = LqProfile.objects.all()

    @list_route(methods=["patch"])
    def edit_detail(self,request,format=None):
        print(request.user.id)
        profile = get_object_or_404(LqProfile,pk=request.user.profile.id)
        data = request.data
        serializer = self.serializer_class(profile,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=400)

    @list_route(methods=["get"])
    def get_user(self, request):
        print(request.user.id,request.META.get('HTTP_AUTHORIZATION'))
        user = get_object_or_404(LqUser, pk=request.user.id)
        serializer = LqUserSerializer(user)
        return Response(serializer.data, status=200)

    # def get_user(self,request,pk=None,format=None):
    #     profile = get_object_or_404(LqProfile,pk=pk)
    #     serializer = self.serializer_class(profile)
    #
    #     return Response(serializer.data,status=200)

# class TokenViewSet(viewsets.ModelViewSet):
