import json

# Create your views here.
from django.http.response import HttpResponse

def method_not_allow():
    return HttpResponse(json.dumps({
        'state':405,
        'msg': 'not found method'
    }),content_type="application/json")

def json_response(data):
    json_data={
        'state': 200,
        'msg':'OK',
        'data':data
    }
    return HttpResponse(json.dumps(json_data),content_type="application/json")

def parma_error(data={}):
    return HttpResponse(
        json.dumps({
            'state':422,
            'msg':'param error',
            'data':data
        }),content_type="application/json"
    )

def server_error():
    return HttpResponse(
        json.dumps({
            'state':500,
            'msg':'server error',
        }),content_type="application/json"
    )

def not_found():
    return HttpResponse(
        json.dumps({
            'state':404,
            'msg':'not found page',
        }),content_type="application/json"
    )

def not_authenticated():
    return HttpResponse(
        json.dumps({
            'state':401,
            'msg':'had not login',
        }),content_type="application/json"
    )

def premission_denied():
    return HttpResponse(
        json.dumps({
            'state':403,
            'msg':'no preission denied',
        }),content_type="application/json"
    )
