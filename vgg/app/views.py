#inbulit libraries
import json
from re import sub

#django imports
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

#rest_frameworf imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

#import from custom files
from .serializers import *
from .authentication import *



@api_view(['GET'])
def landing_page(request):
    context = {
        'message' : "landing page"
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def home_page(request):
    context = {"message": "home page after logging in"}

    return Response(context, status=status.HTTP_200_OK)






@api_view(["GET", "POST"])
def login(request):
    context = {}
    if request.method == 'GET':
        context['message'] = 'login page'
        context['required'] = 'username, password'
        return Response(context, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                JWT.objects.filter(user_id=user.id).delete()
                access = get_access_token({'user_id':user.id})
                refresh = get_refresh_token()
                JWT.objects.create(user_id=user.id, access=access, refresh=refresh)
                context['message'] = 'Login successful!'
                context['access_token'] = access
                context['refresh_token'] = refresh

                return Response(context, status=status.HTTP_202_ACCEPTED)
            else:
                context['error'] = "Invalid login credentials"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context['error'] = serializer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)






@api_view(["GET", "POST"])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def logout(request):
    access = JWT.objects.get(user_id=request.user.id)
    access.delete()

    #the access token should be deleted from frontend

    context = {'message': 'Logout successful'}
    return Response(context, status=status.HTTP_200_OK)







@api_view(["GET", "POST"])
def refresh_login(request):
    context = {}
    if request.method == 'GET':
        context['message'] = 'refresh token page'
        context['required'] = 'refresh_token'
        return Response(context, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = RefreshSerializer(data=request.data)
        if serializer.is_valid():
            try:
                active_token = JWT.objects.get(refresh=serializer.validated_data['refresh_token'])
            except JWT.DoesNotExist:
                context['error'] = 'refresh token not found'
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            if not MyAuthentication.verify_token(serializer.validated_data['refresh_token']):
                context['error'] = 'Token invalid or expired'
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            access = get_access_token({'user_id': active_token.user.id})
            refresh = get_refresh_token()

            active_token.access = access
            active_token.refresh = refresh

            active_token.save()

            context['access_token'] = access
            context['refresh_token'] = refresh

            return Response(context, status=status.HTTP_200_OK)

        else:
            context['error'] = serializer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)











@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated, ))
@authentication_classes((MyAuthentication, ))
def change_password(request):
    if request.method == "GET":
        context = {}
        context['message'] = "Pasword change page"
        context['required'] = "old_password, new_password, new_password_2"

        return Response(context, status=status.HTTP_200_OK)

    if request.method == "POST":
        context = {}
        user = User.objects.get(pk=request.user.id)

        old_password = request.data['old_password']
        new_password = request.data['new_password']
        new_password_2 = request.data['new_password_2']

        if check_password(old_password, user.password):
            if new_password == new_password_2:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                user.save()
                context['message'] = "Password changed successfully"

                return Response(context, status=status.HTTP_200_OK)
            else:
                context['error'] = "new_password and new_password_2 are not the same"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        else:
            context['error'] = "old_password is not correct"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@authentication_classes((MyAuthentication, ))
@permission_classes((IsAuthenticated, ))
def profile_page(request):
    context = {}

    profile = Account.objects.get(user=request.user.id)
    user = User.objects.get(pk=request.user.id)
    profile_serializer = AccountSerializer(profile)
    user_serializer = UserSerializer(user)
    context['profile'] = profile_serializer.data
    context['profile']['user'] = user_serializer.data
    
    return Response(context, status=status.HTTP_200_OK)







@api_view(['GET', 'POST'])
def account_signup(request):
    if request.method == 'GET':
        context = {}
        context['message'] = 'signup page'
        context['required'] = ['first_name', 'last_name',  'username', 'password', 'password_2', 'email', 'interests(array)', 'bio']
        return Response(context, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = AccountSignUpSeralizer(data=request.data)
        context = {}
        if serializer.is_valid():
            new_account = serializer.save()

            context['response'] = 'account created successfully, you can now login with your email and password'
            context['email'] = new_account.user.email

            return Response(context, status=status.HTTP_201_CREATED)

        else:
            context['error'] = serializer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def expert_support(request):
    context= {}
    if request.method== 'GET':
        questions_available= Expert_support.objects.filter(answered=False)
        serializer= ExpertSupportSerializer(questions_available, many= True)
        context['unanswered_expert_questions']= serializer.data
        return Response(context, status.HTTP_200_OK)

    elif request.method == 'POST':
        context= {}
        serializer= ExpertSupportSerializer(data= request.data)
        if request.is_valid():
            new_expert_question= serializer.save()

            context['message'] = 'Your request for expert support has been received and an expert will get in touch with you soon'
            return Response(context, status.HTTP_202_ACCEPTED)

        else:
            context['error'] = serializer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



