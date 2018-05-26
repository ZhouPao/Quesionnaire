from django.conf.urls import url

from Api.view import *
from Api.resources import Register


api=Register()
api.regist(ReigstCodeResource('regist_code'))
api.regist(UserRegistResource('regist'))
api.regist(UserLoginResource('login'))