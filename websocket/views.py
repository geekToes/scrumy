import json
import boto3
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
    return JsonResponse({"message":"disconnected successfully"}, status=200)    

def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url='https://lr3z72e4h0.execute-api.eu-central-1.amazonaws.com/test/',
        region_name='eu-central-1',
        aws_access_key_id='AKIAQBA7ZTETCIYL5VFI',
        aws_secret_access_key='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'
    )
    return gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(data).encode('utf-8')
    )
    
@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    ChatMessage.objects.create(
      username=body['username'],
      message=body['message'],
      timestamp=body['timestamp']
    )
    connections = Connection.objects.all()
    data = {'messages': [body]}
    print(data)
    for connection in connections:
        _send_to_connection(connection.connection_id, data)

    return JsonResponse({"message": "successfully sent"}, status=200)


@csrf_exempt
def recent_messages(request):
  body = _parse_body(request.body)
  connection_id = body['connectionId']
  messages = []
  for message in ChatMessage.objects.all():
    messages.append(
      {
        'username': message.username,
        'message': message.message,
        'timestamp': message.timestamp
      }
    )
  messages.reverse()
  data = { 'messages': messages }
  _send_to_connection(connection_id, data)

  return JsonResponse({'message': 'success'}, status=200)
