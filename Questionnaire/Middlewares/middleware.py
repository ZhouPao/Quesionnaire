import json

from django.http.multipartparser import MultiPartParser
from  django.middleware.common import MiddlewareMixin
from Api.utils import parma_error

class DataConvert(MiddlewareMixin):
    
    def process_request(self,request):
        method=request.method

        if 'application/json' in request.META['CONTENT_TYPE']:
            try:
                data=json.loads(request.body.decode())
            except Exception as e:
                return parma_error({
                    'body':'request data type is error'
                })
        elif 'multipart/form-data' in request.META['CONTENT_TYPE']:
            
            data,files=MultiPartParser(
                request.META,request,request.upload_handlers
            ).parse()
        else:
            data=request.GET
            files=None
        if 'HTTP_X_METHOD' in request.META:
            method=request.META('HTTP_X_METHOD').upper()
            setattr(request,'method',method)
        if files:
            setattr(request,'{method}_FILES'.format(method=method),files)
        setattr(request,method,data)
