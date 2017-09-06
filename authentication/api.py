from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.views import LoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import viewsets
from authentication.serializers import LqProfileSerializer,LqUserSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from authentication.models import LqProfile,LqUser
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.authtoken.models import Token



class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class UserRegistraionViewset(viewsets.ModelViewSet):
    serializer_class = LqProfileSerializer
    permission_classes =(permissions.IsAuthenticatedOrReadOnly,)
    queryset = LqProfile.objects.all()

    def update(self,request,pk=None,format=None):

        profile = get_object_or_404(LqProfile,pk=request.user.profile.id)
        data = request.data
        serializer = self.serializer_class(profile,data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=400)

    @list_route(methods=["get"])
    def get_user(self, request):
        user = get_object_or_404(LqUser, pk=request.user.id)
        serializer = LqUserSerializer(user)
        return Response(serializer.data, status=200)

    # def get_user(self,request,pk=None,format=None):
    #     profile = get_object_or_404(LqProfile,pk=pk)
    #     serializer = self.serializer_class(profile)
    #
    #     return Response(serializer.data,status=200)

# class TokenViewSet(viewsets.ModelViewSet):
