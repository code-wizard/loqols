from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from authentication import api


pr = routers.SimpleRouter()
pr.register("",api.UserRegistraionViewset,"pr")

urlpatterns = [
    url(r'^api/v1/profile/',include(pr.urls,namespace="pr-api")),

]



