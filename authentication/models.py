from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None,username="default", **kwargs):
        try:
            user = self.model(
                email=self.normalize_email(email),
                is_active=True,
                **kwargs
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError:
            return

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class LqUser(AbstractBaseUser,PermissionsMixin):
    USERNAME_FIELD ="email";
    REQUIRED_FIELDS= []
    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)
    username = models.CharField(_('username'),max_length=500,blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table="lq_user"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return "%s" % (self.get_full_name())


def photo_upload_path(instance,filename):
    return "".join(["%s%s%s%s" %("profile-photo/",str(instance.first_name),str(instance.last_name),"/"),filename])


class LqProfile(models.Model):
    user = models.OneToOneField(LqUser, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=16, null=True,blank=True)
    dob = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=2, null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=50)
    gender = models.CharField(max_length=10, blank=True, null=True)
    marital_status = models.CharField(max_length=10, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    has_photo = models.BooleanField(default=False)
    avatar = models.ImageField(blank=True,null=True, default="avatar_male.png", upload_to=photo_upload_path)

    def save(self,*args,**kwargs):
        if self.gender == "Male" and not self.has_photo:
            self.avatar = "avatar_male.png"
        elif self.gender == "Female" and not self.has_photo:
            self.avatar = "avatar_female.png"
        super(LqProfile,self).save(*args,**kwargs)

    class Meta:
        db_table = "lq_profile"


class LqGeneralSetting(models.Model):
    OPTION_1 = (
        (1, "Off"),
        (2, "People I follow"),
        (3, "Everyone")
    )
    user = models.OneToOneField(LqUser,on_delete=models.CASCADE, related_name="settings")
    who_can_event = models.PositiveIntegerField(choices=OPTION_1,default=1)
    private_account = models.BooleanField(default=False)
    language = models.CharField(max_length=255,default="English")

    class Meta:
        db_table = "lq_general_setting"


class LqPushNotificationSetting(models.Model):
    OPTION_1 =(
        (1,"Off"),
        (2,"People I follow"),
        (3,"Everyone")
    )
    OPTION_2=(
        (1,"On"),
        (2,"Off")
    )
    comments = models.PositiveIntegerField(default=3,choices=OPTION_1)
    new_follower = models.PositiveIntegerField(default=1,choices=OPTION_2)
    reminder = models.PositiveIntegerField(default=1,choices=OPTION_2)
    message = models.PositiveIntegerField(default=1,choices=OPTION_2)
    likes = models.PositiveIntegerField(default=3,choices=OPTION_1)
    new_event = models.PositiveIntegerField(default=3, choices=OPTION_1)
    comment_likes = models.PositiveIntegerField(default=3, choices=OPTION_1)

    class Meta:
        db_table = "lq_push_notification"


class LqFollows(models.Model):
    follower = models.ForeignKey(LqUser,on_delete=models.CASCADE,related_name="followers")
    following = models.ForeignKey(LqUser,on_delete=models.CASCADE,related_name="following")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lq_follows"
