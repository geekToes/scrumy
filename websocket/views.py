import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Connection
from .models import ChatMessage
# Create your views here.


@csrf_exempt
def test(request):
    return JsonResponse({'message': 'hello Daud'}, status=200)


def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)

@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connection = Connection.objects.create(connection_id=connection_id)
    connection.save()
    return JsonResponse({"message":"connected successfully"}, status=200)
@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connection = Connection.objects.get(connection_id=connection_id).delete()
    connection.save()
    return JsonResponse({"message":"disconnected successfully"}, status=200)    