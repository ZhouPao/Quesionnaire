from Api.utils import *

#login user must customer and only use in class
def customer_required(func):
    def _wrapper(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return not_authenticated()
        user=request.user
        if not hasattr(user,'customer'):
            return premission_denied()
        return func(self,request,*args,**kwargs)
    return _wrapper

#login user must userifo and only use in class
def userinfo_required(func):
    def _wrapper(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return not_authenticated
        user=request.user
        if not hasattr(user,'userinfo'):
            return premission_denied()
        return func(self,request,*args,**kwargs)
    return _wrapper

##login user must superuser and only use in class
def superuser_required(func):
    def _wrapper(self,request,*args,**kwargs):
        if not request.user.is_superuser:
            return not_authenticated()
        return func(self,request,*args,**kwargs)
    return _wrapper