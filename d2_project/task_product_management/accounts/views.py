from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.serializer import RegisterSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

# Register view
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View (JWT Authentication)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# Forgot Password View
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            reset_url = f'http://localhost:8000/reset-password/{uid}/{token}/'  
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                'noreply@example.com',
                [email],
            )
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response({"message": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

# Reset Password View
class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except Exception:
            return Response({"message": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
