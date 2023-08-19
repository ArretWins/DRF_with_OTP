from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, VerifyAccountSerializer
from .emails import send_otp_via_email

class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'registration successfully check email',
                    'data': serializer.data,

                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'invalid email'
                    })

                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'wrong OTP'
                    })
                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': 'account verified',
                    'data': {},

                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)



class CustomLoginView(APIView):
    def post(self, request):
        # username = None
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)

        check_user = User.objects.filter(email = email).exists()
        if check_user == False:
            return Response({"error": "Username does not exists"}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request,user)
            token, created = Token.objects.get_or_create(user=request.user)
            data = {
                'token': token.key,
                'user_id': request.user.pk,
                'email':request.user.email
            }
            return Response({"success": "Successfully login", "data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email detect"}, status=status.HTTP_400_BAD_REQUEST)


@action(detail=False, methods=['post'])
def CustomLogoutView(self, request):
    print(999)       #Nothing
    try:
        print(request.user.auth_token)
        request.user.auth_token.delete()
    except (AttributeError):
        pass
    from django.contrib.auth import logout
    logout(request)

    return Response({"success": "Successfully logged out."},
                    status=status.HTTP_200_OK)


class ShowApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
