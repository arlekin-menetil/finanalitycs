from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from profiles.models import FinancialProfile


# ==========================================
# PHONE
# ==========================================

def normalize_phone(phone):

    return "".join(filter(str.isdigit, phone))


# ==========================================
# SEND CODE
# ==========================================

class SendCodeAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        phone = request.data.get("phone")

        if not phone:

            return Response(
                {
                    "error": "Phone required"
                },
                status=400
            )

        phone = normalize_phone(phone)

        if len(phone) != 12:

            return Response(
                {
                    "error": "Invalid phone format"
                },
                status=400
            )

        code = "123456"

        print(
            f"DEV LOGIN {phone} -> {code}"
        )

        return Response({

            "message": "Code sent",

            "dev_code": code

        })


# ==========================================
# VERIFY
# ==========================================

class VerifyCodeAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        phone = normalize_phone(

            request.data.get("phone", "")

        )

        code = request.data.get("code")

        if not phone or not code:

            return Response(
                {
                    "error":"Phone and code required"
                },
                status=400
            )

        if code != "123456":

            return Response(
                {
                    "error":"Invalid code"
                },
                status=400
            )

        user, created = User.objects.get_or_create(

            phone_number=phone,

            defaults={

                "is_active":True

            }

        )

        if not user.is_active:

            user.is_active = True
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response({

            "user_id":user.id,

            "phone":user.phone_number,

            "access":str(refresh.access_token),

            "refresh":str(refresh)

        })


# ==========================================
# ME
# ==========================================

class MeAPIView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def get(self, request):

        user = request.user

        profile = FinancialProfile.objects.filter(

            user=user

        ).first()

        profile_completed = False

        if profile:

            profile_completed = (

                profile.is_profile_completed

            )

        return Response({

            "user_id":user.id,

            "phone":user.phone_number,

            "is_profile_completed":profile_completed,

            "profile":{

                "exists":profile is not None

            }

        })