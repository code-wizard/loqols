from rest_framework import serializers
from authentication.models import LqUser,LqProfile,LqFollows,LqGeneralSetting,LqPushNotificationSetting
from allauth.account.adapter import get_adapter
from django.db import  transaction

class LqProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = LqProfile
        fields = "__all__"


class LqUserSerializer(serializers.ModelSerializer):
    profile = LqProfileSerializer(required=False)

    class Meta:
        model = LqUser
        fields = "__all__"


class LqUserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=255, required=False)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=16, required=False)
    dob = serializers.DateField(required=False)
    country = serializers.CharField(max_length=2, required=False)
    city = serializers.CharField(required=False, max_length=50)
    gender = serializers.CharField(max_length=10,required=False)
    marital_status = serializers.CharField(max_length=10, required=False)
    avatar = serializers.ImageField(required=False)

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

