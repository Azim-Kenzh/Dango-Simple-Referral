from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Referral, Profile
import random
import string
import time
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, ActivateInviteCodeSerializer


def generate_invite_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def send_verification_code(phone_number):
    # Имитация отправки кода с задержкой 1-2 секунды
    time.sleep(random.uniform(1, 2))
    return ''.join(random.choices(string.digits, k=4))


class AuthenticateView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: 'Verification code sent successfully'},
        operation_summary="Authenticate user and send verification code",
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            # Генерируем новый код верификации
            verification_code = send_verification_code(phone_number)

            # Создаем или обновляем профиль пользователя
            user, created = User.objects.get_or_create(username=phone_number)
            profile, created = Profile.objects.get_or_create(user=user, phone_number=phone_number)
            profile.verification_code = verification_code
            profile.save()

            return JsonResponse({'status': 'success', 'verification_code': verification_code})
        else:
            return JsonResponse({'status': 'error', 'message': 'Phone phone_number is required'})


class VerifyCodeView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'verification_code': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        if not phone_number or not verification_code:
            return JsonResponse({'status': 'error', 'message': 'phone_number and verification_code are required'})

        try:
            # Получаем профиль пользователя по номеру телефона
            profile = Profile.objects.get(phone_number=phone_number)
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'})

        if profile.verification_code != verification_code:
            return JsonResponse({'status': 'error', 'message': 'Invalid verification code'})

        # # Если верификация прошла успешно, сбрасываем код верификации
        # profile.verification_code = None
        # profile.save()

        # Генерируем или возвращаем инвайт-код
        if not profile.invite_code:
            invite_code = generate_invite_code()
            profile.invite_code = invite_code
            profile.save()
        else:
            invite_code = profile.invite_code

        token, created_token = Token.objects.get_or_create(user=profile.user)

        return JsonResponse({
            'status': 'success',
            'invite_code': invite_code,
            'token': token.key  # Отправляем ключ токена для входа в Профиль и Подтверждении инвайт кода
        })


class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        profile = queryset.first()

        # Получаем список пользователей, которые активировали код приглашения текущего пользователя
        referred_users = Profile.objects.filter(referrals_received__referrer=profile).values_list('phone_number',
                                                                                                  flat=True)

        serializer = self.get_serializer(profile)
        return Response({
            'phone_number': serializer.data['phone_number'],
            'invite_code': serializer.data['invite_code'],
            'referred_users': list(referred_users)
        }
        )


class ActivateInviteCodeView(generics.GenericAPIView):
    serializer_class = ActivateInviteCodeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invite_code = serializer.validated_data.get('invite_code')
        user = request.user

        referred_profile = Profile.objects.filter(invite_code=invite_code).first()

        if not referred_profile:
            return Response({'status': 'error', 'message': 'Invalid invite code.'}, status=status.HTTP_400_BAD_REQUEST)

        if referred_profile == user.profile:
            return Response({'status': 'error', 'message': 'You cannot activate your own invite code.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, есть ли уже запись о реферрале для данного пользователя
        existing_referral = Referral.objects.filter(referrer=referred_profile, referred=user.profile).exists()
        if existing_referral:
            return Response({'status': 'error', 'message': 'Invite code already used.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Активируем инвайт-код
        user.profile.invite_code = invite_code
        user.profile.save()

        # Создаем запись о реферрале
        Referral.objects.create(referrer=referred_profile, referred=user.profile)

        return Response({'status': 'success', 'message': 'Invite code activated successfully.'},
                        status=status.HTTP_200_OK)
