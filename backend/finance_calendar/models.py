from django.db import models
from django.conf import settings


class CalendarEvent(models.Model):
    EVENT_TYPES = [
        ("payment", "Payment"),
        ("reminder", "Reminder"),
        ("credit", "Credit"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="calendar_events"
    )

    title = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    date = models.DateField()

    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date})"