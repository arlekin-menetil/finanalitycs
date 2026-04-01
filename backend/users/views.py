from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# ============================
# HELPER
# ============================

def normalize_phone(phone):
    return "".join(filter(str.isdigit, phone))


# ============================
# 📩 SEND CODE (DEV MODE)
# ============================

class SendCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response({"error": "Phone required"}, status=400)

        phone = normalize_phone(phone)

        if len(phone) != 12:
            return Response({"error": "Invalid phone format"}, status=400)

        # 💣 DEV режим — просто лог
        print(f"📩 DEV MODE: code 000000 for {phone}")

        return Response({
            "message": "Code sent (DEV MODE)"
        })


# ============================
# 🔢 VERIFY CODE (DEV MODE)
# ============================

class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")

        if not phone or not code:
            return Response({"error": "Phone and code required"}, status=400)

        phone = normalize_phone(phone)

        # 💣 универсальный код
        if code != "000000":
            return Response({"error": "Invalid code"}, status=400)

        user, _ = User.objects.get_or_create(phone_number=phone)

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user_id": user.id,
            "phone": user.phone_number,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


# ============================
# 👤 ME
# ============================

class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        profile_completed = False

        if hasattr(user, "financial_profile"):
            profile_completed = user.financial_profile.is_profile_completed

        return Response({
            "user_id": user.id,
            "phone": user.phone_number,
            "is_profile_completed": profile_completed
        })