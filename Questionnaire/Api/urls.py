from django.conf.urls import url

from Api.view import *
from Api.resources import Register


api=Register()
api.regist(ReigstCodeResource('regist_code'))
api.regist(UserRegistResource('regist'))
api.regist(UserLoginResource('login'))
api.regist(QuestionnaireResource('questionnaire'))
api.regist(QustionResource('requestion'))
api.regist(QuestionnaireCommentResource('questionnaire_comment'))
api.regist(QuestionnaireStateResource('questionnaire_state'))
api.regist(AnswerResource('answer'))





