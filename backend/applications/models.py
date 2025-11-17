from django.db import models


class ApplicationStatus(models.TextChoices):
    NEW = "NEW", "Новая"
    IN_PROGRESS = "IN_PROGRESS", "В обработке"
    APPROVED = "APPROVED", "Одобрена"
    REJECTED = "REJECTED", "Отклонена"


class Application(models.Model):
    imei = models.CharField("IMEI", max_length=15)
    phone = models.CharField("Номер телефона", max_length=16)
    passport = models.CharField("Номер паспорта", max_length=50, blank=True, null=True)

    application_number = models.CharField(
        "Номер заявки",
        max_length=20,
        unique=True,
        editable=False,
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.application_number} ({self.imei})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.application_number:
            # простая схема: #ID с нулями
            self.application_number = f"{self.id:05d}"
            super().save(update_fields=["application_number"])