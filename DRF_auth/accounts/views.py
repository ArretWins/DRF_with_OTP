from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, VerifyAccountSerializer
from .emails import send_otp_via_email

class RegisterAPI(APIView):
    def get(self, request):
        return render(request, 'accounts/registration.html')
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

    def get(self, request):
        return render(request, 'accounts/verify.html')

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

    def get(self, request):
        # Проверка, авторизован ли пользователь
        if request.user.is_authenticated:
            context = {'logout_message': 'You are already logged in. Please log out before attempting to log in again.'}
            return render(request, 'accounts/logout.html', context)

        context = {
            'logout_message': '',
            'email': ''  # Очищаем поле email
        }
        return render(request, 'accounts/login.html', context)

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


class CustomLogoutView(APIView):
    def get(self, request):
        return render(request, 'accounts/logout.html')


    def post(self, request):
        if request.user.is_authenticated:
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
            except Token.DoesNotExist:
                pass
            from django.contrib.auth import logout
            logout(request)
            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not logged in."}, status=status.HTTP_401_UNAUTHORIZED)


class ShowApi(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Дополнительные фильтры и сортировка, если нужно
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        return render(request, 'accounts/user_list.html', {'object_list': users, 'current_user': request.user})


@csrf_exempt
@login_required
def DeleteProfileView(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)  # Разлогиниваем пользователя
        return redirect('custom-login')  # Перенаправляем на страницу входа

    return render(request, 'accounts/delete_profile.html')