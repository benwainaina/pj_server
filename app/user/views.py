from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from user.models import UserModel
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def create_account(request: Request):
    payload = get_data_object_from_request(request)
    response = Response()
    fullname = payload.get('fullname')
    email = payload.get('email')
    password = payload.get('password')
    if not fullname or not email or not password:
        response.status_code = 500
        response.data = {'status': 'INVALID_DATA'}
    else:
        try:
            user_instance = UserModel.objects.create(
                fullname = fullname,
                email = email,
                user_ref=User.objects.create(username=email, email=email, password=make_password(password))
            )
            Token.objects.create(user=user_instance.user_ref)
            response.status_code = 200
            response.data = {'status': 'ACCOUNT_CREATED'}
        except Exception as e:
            print('e', str(e))
            response.status_code = 500
            response.data = {'status': 'USER_ALREADY_EXISTS'}
    return response

@api_view(['POST'])
def login(request):
    data = get_data_object_from_request(request)
    response = Response()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        response.status_code = 400
        response.data = {'status': 'INVALID_CREDENTIALS'}
    else:
        try:
            user_instance = UserModel.objects.get(email=email)
            if check_password(password, user_instance.user_ref.password):
                try:
                    Token.objects.get(user=user_instance.user_ref).delete()
                except:
                    pass
                user_token = Token.objects.create(user=user_instance.user_ref)
                response.status_code = 200
                response.data = {'token': user_token.key, 'status': 'SUCCESS'}
            else:
                response.status_code = 500
                response.data = {'status': 'INVALID_CREDENTIALS'}
        except Exception as e:
            response.status_code = 500
            response.data = {'status': 'ACCOUNT_DOES_NOT_EXIST'}
    return response

@api_view(['POST'])
def validate_token(request):
    response = Response()
    data = get_data_object_from_request(request)
    token = data.get('token')
    if not token:
        response.status_code = 400
        response.data = {'status': 'INVALID_DATA'}
    else:
        try:
            token_instance = Token.objects.get(key=token)
            user_instance = UserModel.objects.get(user_ref=token_instance.user)
            response.status_code = 200
            response.data = {
                'fullname': user_instance.fullname,
                'email': user_instance.email,
            }
        except:
            response.status_code = 500
            response.data = {'status': 'INVALID_DATA'}
    return response

@api_view(['POST'])
def update_profile(request):
    response = Response()
    data = get_data_object_from_request(request)
    token = data.get('token')
    fullname = data.get('fullname')
    password = data.get('password')
    if not fullname or not password:
        response.status_code = 400
        response.data = {'status': 'INVALID_DATA'}
    else:
        try:
            user_instance = UserModel.objects.get(
                user_ref=Token.objects.get(key=token).user
            )
            user_instance.fullname = fullname
            user_instance.user_ref.password = make_password(password)
            user_instance.save()
            response.status_code = 200
            response.data = {'status': 'SUCCESS'}
        except Exception as e:
            response.status_code = 500
            response.data = {'status': 'INTERNAL_SERVER_ERROR'}
    return response


# COMMON METHODS
def get_data_object_from_request(request):
    return request.data
