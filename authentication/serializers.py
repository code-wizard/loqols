
from authentication.models import LqUser,LqProfile,LqFollows,LqGeneralSetting,LqPushNotificationSetting
from allauth.account.adapter import get_adapter
from django.db import transaction
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_auth.models import TokenModel


UserModel = get_user_model()


class LqProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = LqProfile
        fields = ["id","first_name","last_name","phone","dob","country","city","gender","marital_status","updated_at",
                  "created_at","avatar"]


class LqUserSerializer(serializers.ModelSerializer):
    profile = LqProfileSerializer(required=False)


    class Meta:
        model = LqUser
        fields = ["id","profile","email","is_staff","is_active","date_joined"]


class LqUserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)


    def validate_email(self,email):
        return get_adapter().clean_email(email)

    def validate_password(self,password):
        return get_adapter().clean_password(password)

    def validate_phone(self,phone):
        return phone

    def save(self,request):
        with transaction.atomic():
            adapter = get_adapter()
            user = adapter.new_user(request)
            # self.cleaned_data = self.get_cleaned_data()
            self.cleaned_data=self.validated_data
            adapter.save_user(request, user, self)
            LqProfile.objects.create(
                first_name=self.validated_data.get('first_name'),
                last_name=self.validated_data.get('last_name'),
                user=user
            )
            # setup_user_email(request, user, [])
            return user


    class Meta:
        # model = LqUser
        fields = "__all__"


class LqLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user


    # def _validate_username_email(self, username, email, password):
    #     user = None
    #
    #     if email and password:
    #         user = authenticate(email=email, password=password)
    #     else:
    #         msg = _('Must include either "username" or "email" and "password".')
    #         raise exceptions.ValidationError(msg)
    #
    #     return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        username=None

        user = None
        user = self._validate_email(email, password)
        # if 'allauth' in settings.INSTALLED_APPS:
        #     from allauth.account import app_settings
        #
        #     # Authentication through email
        #     # if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
        #     user = self._validate_email(email, password)

            # # Authentication through username
            # if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
            #     user = self._validate_username(username, password)

            # Authentication through either username or email
            # else:
            #     user = self._validate_username_email(username, email, password)

        # else:
        #     # Authentication without using allauth
        #     if email:
        #         try:
        #             username = UserModel.objects.get(email__iexact=email).get_username()
        #         except UserModel.DoesNotExist:
        #             pass
        #
        #     if username:
        #         user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class LqTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = LqUserSerializer(required=False)

    class Meta:
        model = TokenModel
        fields = ('key','user')