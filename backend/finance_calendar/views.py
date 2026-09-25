from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import date

from .models import CalendarEvent


class CalendarEventsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # ==========================================
        # 💣 СОЗДАЁМ СОБЫТИЕ РЕГИСТРАЦИИ (1 раз)
        # ==========================================
        if user.date_joined:
            CalendarEvent.objects.get_or_create(
                user=user,
                title="Регистрация в системе",
                event_type="reminder",
                date=user.date_joined.date()
            )

        # ==========================================
        # 📅 ПОЛУЧАЕМ СОБЫТИЯ
        # ==========================================
        events = (
            CalendarEvent.objects
            .filter(user=user)
            .order_by("date")  # 🔥 сортировка по дате
        )

        # ==========================================
        # 🧠 ФОРМИРУЕМ ОТВЕТ
        # ==========================================
        data = []

        for e in events:
            data.append({
                "id": e.id,
                "title": e.title,
                "start": str(e.date),  # 💣 для календаря (ISO)
                "amount": float(e.amount or 0),
                "type": e.event_type,
                "completed": e.is_completed,
            })

        return Response(data)