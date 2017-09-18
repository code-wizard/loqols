from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from authentication import api


pr = routers.SimpleRouter()
pr.register("",api.UserRegistraionViewset,"pr")

check_auth = routers.SimpleRouter()
check_auth.register("",api.CheckAuth,"check-auth")

urlpatterns = [
    url(r'^api/v1/profile/',include(pr.urls,namespace="pr-api")),
    url(r'api/v1/check-auth/',include(check_auth.urls,namespace="check-auth")),

]



