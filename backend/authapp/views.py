import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneAuth

User = get_user_model()


# 📩 SEND CODE
@api_view(["POST"])
def send_code(request):
    phone = request.data.get("phone")

    if not phone:
        return Response({"error": "Введите номер"}, status=400)

    # 🔥 генерим код
    code = str(random.randint(100000, 999999))

    # 🔥 сохраняем или обновляем
    obj, _ = PhoneAuth.objects.get_or_create(phone=phone)
    obj.code = code
    obj.save()

    print(f"DEV CODE for {phone}: {code}")

    return Response({
        "message": "Код отправлен",
        "dev_code": code  # убрать в проде
    })


# 🔢 VERIFY CODE
@api_view(["POST"])
def verify_code(request):
    phone = request.data.get("phone")
    code = request.data.get("code")

    if not phone or not code:
        return Response({"error": "Неверные данные"}, status=400)

    try:
        obj = PhoneAuth.objects.get(phone=phone, code=code)
    except PhoneAuth.DoesNotExist:
        return Response({"error": "Неверный код"}, status=400)

    # 🔥 создаём или берём пользователя
    user, created = User.objects.get_or_create(phone=phone)

    # 🔥 JWT
    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user_id": user.id,
        "phone": user.phone
    })