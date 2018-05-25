from django.shortcuts import render
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Api.utils import method_not_allow

# Create your views here.
class Resource(object):
    
    def __init__(self, name,*args, **kwargs):
        self.name=name or self.__class__.__name__.lower()
    
    #This is url entry
    def enter(self,request,*args,**kwargs):

        method=request.method
        
        if method=='GET':
            response=self.get(self,request,*args,**kwargs)
        elif method=='POST':
            response=self.post(self,request,*args,**kwargs)
        elif method=='PUT':
            response=self.post(self,request,*args,**kwargs)
        elif method=='DELETE':
            response=self.delete(response=self.post(self,request,*args,**kwargs))
        elif method=='HEAD':
            response=self.head(response=self.post(self,request,*args,**kwargs)) 
        elif method=='OPTIONS':
            response=self.options(response=self.post(self,request,*args,**kwargs))
        else:
            response=method_not_allow()
        return response
    
    def get(self,request,*args,**kwargs):
        method_not_allow()
    
    def post(self,request,*args,**kwargs):
        method_not_allow()
    
    def put(self,request,*args,**kwargs):
        method_not_allow()
    
    def delete(self,request,*args,**kwargs):
        method_not_allow()
    
    def head(self,request,*args,**kwargs):
        method_not_allow()
    
    def options(self,request,*args,**kwargs):
        method_not_allow()

class Register(object):
    
    def __init__(self, version='v1', *args, **kwargs):
        self.version=version
        self.resources=[]
    
    def regist(self,resource):
        self.resources.append(resource)
    
    @property
    def urls(self):
        urlpatterns=[]
        for resource in self.resources:
            urlpatterns.append(
                url(r'^{version}/{name}$'.format(version=self.version,name=resource.name),csrf_exempt(resource.enter))
            )
        return urlpatterns

        
