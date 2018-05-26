import random
import json
import math
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone

from Question.models import *
from Api.resources import Resource
from Api.utils import *


# get regist code
class ReigstCodeResource(Resource):
    def get(self, request, *args, **kwargs):
        regist_code = random.randint(10000, 100000)
        request.session['regist_code'] = regist_code
        return json_response({
            'regist_code': regist_code
        })


# user message
class UserRegistResource(Resource):
    # get user message
    def get(self, request, *args, **kwargs):
        # data=request.GET
        user = request.user
        if request.user.is_authenticated:
            if hasattr(user,'customer'):
                customer=user.customer
                #create user dict
                data=dict()
                data['user']=user.id
                data['name']=getattr(customer,'name','')
                data['email']=getattr(customer,'email','')
                data['company']=getattr(customer,'company','')
                data['address']=getattr(customer,'address','')
                data['phone']=getattr(customer,'phone','')
                data['mobile']=getattr(customer,'mobile','')
                data['qq']=getattr(customer,'qq','')
                data['wechat']=getattr(customer,'wechat','')
                data['web']=getattr(customer,'web','')
                data['industry']=getattr(customer,'industry','')
                data['description']=getattr(customer,'description','')
                return json_response(data)
            elif hasattr(user,'userinfo'):
                userinfo=user.userinfo
                data=dict()
                data['user']=user.id
                data['name']=getattr(userinfo,'name','')
                data['age']=getattr(userinfo,'age','')
                data['gender']=getattr(userinfo,'gender','')
                data['phone']=getattr(userinfo,'phone','')
                data['email']=getattr(userinfo,'email','')
                data['address']=getattr(userinfo,'address','')
                if userinfo.birthday:
                    data['birthday']=userinfo.birthday.strftime('%Y-%m-%d')
                else:
                    data['birthday']=datetime.now().strftime('%Y-%m-%d')
                data['qq']=getattr(userinfo,'qq','')
                data['wechat']=getattr(userinfo,'wechat','')
                data['job']=getattr(userinfo,'job','')
                data['salary']=getattr(userinfo,'salary','')
                return json_response(data)
            else:
                json_response({})
            return json_response({
                'msg':'get user message success'
            })
        # if not login can not scanner 
        return not_authenticated()

    # regist user
    def put(self, request, *args, **kwargs):
        data = request.PUT
        username = data.get('username', '')
        password = data.get('password', '')
        regist_code = data.get('regist_code', '')
        session_regist_code = request.session.get('regist_code', 1111111)
        category = data.get('category', 'userinfo')
        ensure_password = data.get('ensure_password', '')

        # create errors dict
        errors = dict()
        if not username:
            errors['username'] = '没有提供用户名'
        elif User.objects.filter(username=username):
            errors['username'] = '用户名已存在'
        if len(password) < 6:
            errors['password'] = '密码长度不够'
        if password != ensure_password:
            errors['ensure_password'] = '密码不一样'
        if regist_code != str(session_regist_code):
            errors['regist_code'] = '验证码不对'
        if errors:
            return params_error(errors)
        user = User()
        user.username = username
        # settin password
        user.set_password(password)
        user.save()
        # judge user category create userinfo or customer
        if category == 'userinfo':
            userinfo = UserInfo()
            userinfo.user = user
            userinfo.name = '姓名'
            userinfo.save()
        else:
            customer = Customer()
            customer.name = '客户名称'
            customer.user = user
            customer.save()
        login(request, user)
        return json_response({
            "id": user.id
        })

    # update user message
    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        if user.is_authenticated:
            if hasattr(user,'userinfo'):
                userinfo=user.userinfo
                userinfo.user=data.get('user','')
                userinfo.name=data.get('name','')
                userinfo.age=data.get('age','')
                userinfo.gender=data.get('gender','')
                userinfo.phone=data.get('phone','')
                userinfo.email=data.get('email','')
                userinfo.address=data.get('address','')
                try:
                    birthday=datetime.strftime(data.get('birthday','2018-01-01'),'%Y-%m-%d')
                except Exception as e:
                    birthday=datetime.now()
                userinfo.birthday=birthday
                userinfo.qq=data.get('qq','')
                userinfo.wechat=data.get('wechat','')
                userinfo.job=data.get('job','')
                userinfo.salary=data.get('salary','')
                userinfo.save()
            elif hasattr(user,'customer'):
                customer=user.customer
                customer.name=data.get('name','')
                customer.email=data.get('email','')
                customer.company=data.get('company','')
                customer.address=data.get('address','')
                customer.phone=data.get('phone','')
                customer.mobile=data.get('mobile','')
                customer.qq=data.get('qq','')
                customer.wechat=data.get('wechat','')
                customer.web=data.get('web','')
                customer.industry=data.get('industry','')
                customer.description=data.get('description','')
                customer.save()
            return json_response({
                'msg':'update success'
            })
                
        return not_authenticated()


# user login and logout
class UserLoginResource(Resource):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return json_response({
                'user_id':'had login'
            })
        return not_authenticated

    def put(self, request, *args, **kwargs):
        data=request.PUT
        username=data.get('username','')
        password=data.get('password','')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return json_response({
                'msg':'login is success'
            })
        return parma_error({
            'msg':'username or password is error'
        })

    def delete(self, request, *args, **kwargs):
        logout(request)
        return json_response({
            'msg':'logout is success'
        })


class QuestionnaireResource(Resource):

    def get(self,request,*args,**kwargs):
        data=request.GET
        state=data.get('state',False)
        limit=abs(int(data.get('state',15)))
        start_id=data.get('start_id',False)
        title=data.get('title',False)
        create_time=data.get('create_time',False)

        Qs=[]
        if state:
            state=[int(state)]
        else:
            sate=[0,1,2,3,4]
        Qs.append(Q(state__in=state))
        
        if start_id:
            start_id=int(start_id)
        else:
            start_id=0
        Qs.append(Q(id__gt=start_id))
        if title:
            Qs.append(Q(title__contains=title))
        if create_time:
            create_time=datetime.strftime(create_time,'%Y-%m-%d')
            Qs.append(Q(datetime__gt=create_time))
        
        Qs.append(Q(customer=request.user.customer))

        if limit > 50:
            limit=50
        
        objs=Questionnaire.objects.filter(*Qs)[:limit]

        data=[]
        for obj in objs:
            #create one questionnaire formations
            obj_dict=dict()
            obj_dict['id']=obj.id
            obj_dict['title']=obj.title
            obj_dict['logo']=obj.logo
            obj_dict['datetime']=datetime.strftime(obj.datetime,"%Y-%m-%d")
            obj_dict['deadline']=datetime.strftime(obj.deadline,"%Y-%m-%d")
            obj_dict['catogory']=obj.catogory
            obj_dict['state']=obj.state
            obj_dict['quantity']=obj.quantity
            obj_dict['background']=obj.background
            obj_dict['marks']=[{'id':mark.id,'name':mark.name,'description':mark.description} for mark in objs.marks.all()]

            #create questionnaire these question
            obj_dict['questions']=[]
            for question in obj.question_set.all():
                #create one question
                question_dict=dict()
                question_dict['id']=qustion.id
                question_dict['title']=qustion.title
                question_dict['is_checkbox']=qustion.is_checkbox
                question_dict['items']=qustion=[{
                    'id':item.id,
                    'content':item.content
                } for item in question.questionitem_set.all()]
                #question put in questionnaire list
                obj_dict['questions'].append(question_dict)
            
            #questionnaire put in questionnaire list
            data.append(obj_dict)
        return json_response(data)


    def post(self,request,*args,**kwargs):
        data=request.POST
        questionnaire_id=int(data.get('requestionnaire_id',0))
        try:
            questionnaire=Questionnaire.objects.filter(id=questionnaire_id,
                    customer=request.user.customer,state__in=[0,1,2,3])
        except Exception as e:
            return parma_error({
                'requestionnaire_id':'not found this questionnaire'
            })
        
        questionnaire.title=data.get('title','')
        questionnaire.logo=data.get('logo','')
        questionnaire.datetime=datetime.now()
        try:
            deadline_str=data.get('deadline','')
            deadline=datetime.strftime(deadline_str,"%Y-%m-%d")
        except Exception as e:
            deadline=datetime.now()+timedelta(days=10)
        questionnaire.deadline=deadline
        questionnaire.catogory=data.get('catogory','default')
        state=data.get('state',0)
        if state not in [0,1]:
            return parma_error({
                'state':'the state not software'
            })
        questionnaire.state=state
        questionnaire.quantity=data.get('quantity',1)
        questionnaire.background=data.get('background','')
        questionnaire.free_count=data.get('free_count',1)
        questionnaire.save()
        return json_response({
            'msg':'update requestionnaire is success!'
        })
            
    def put(self,request,*args,**kwargs):
        data=request.PUT
        questionnaire=Questionnaire()
        questionnaire.customer=request.user.customer
        questionnaire.title=data.get('title','')
        questionnaire.logo=data.get('logo','')
        questionnaire.datetime=datetime.now()
        try:
            deadline_str=data.get('deadline','')
            deadline=datetime.strftime(deadline_str,"%Y-%m-%d")
        except Exception as e:
            deadline=datetime.now()+timedelta(days=10)
        questionnaire.deadline=deadline
        questionnaire.catogory=data.get('catogory','default')
        questionnaire.state=0
        questionnaire.quantity=data.get('quantity',1)
        questionnaire.background=data.get('background','')
        questionnaire.free_count=data.get('free_count',1)
        questionnaire.save()
        # seve the questionnaire now create the mark
        #get the list of label ID that you need to add to the questionnaire
        mark_ids=data.get('mark_ids',[])
        marks=Mark.objects.filter(id__in=mark_ids)
        # This we can add to judge if have marks questionnaire add mark
        # if marks:
        questionnaire.marks.set(marks)
        questionnaire.save()

        return json_response({
            'questionnaire_id':questionnaire.id
        })
            
    def delete(self,request,*args,**kwargs):
        data =request.DELETE
        ids=data.get('ids',[])
        objs=Questionnaire.objects.filter(id__in=ids,customer=request.user.customer,state__in=[0,1,2,3])
        deleted_ids=[obj.id for obj in objs]
        objs.delete()
        return json_response({
            'deleted_ids':deleted_ids
        })