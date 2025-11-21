from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import Application

def index(request):
    return render(request, "applications/index.html")

def create_application(request):
    if request.method == "POST":
        imei = request.POST.get("imei", "").strip()
        phone = request.POST.get("phone", "").strip()
        passport = request.POST.get("passport", "").strip()

        # Валидация
        if not (imei.isdigit() and len(imei) == 15):
            return render(request, "applications/index.html", {
                "error": _("Некорректный IMEI."),
            })

        if not (phone.startswith("+7") and len(phone) == 12 and phone[2:].isdigit()):
            return render(request, "applications/index.html", {
                "error": _("Некорректный номер телефона."),
            })

        # Атомарная попытка создать или получить существующую
        with transaction.atomic():
            application, created = Application.objects.get_or_create(
                imei=imei,
                defaults={
                    "phone": phone,
                    "passport": passport or None,
                },
            )

        if not created:
            # ВАЖНО: сначала переводим строку, потом форматируем
            info_msg = _("Компания прошла квалификационные требования и начнёт обработку заявок после подписания соглашения с РГП ГРС")
            return render(request, "applications/index.html", {
                "info": info_msg,
            })

        # Новая заявка — показываем success
        message = _(
            "Компания прошла квалификационные требования и начнёт обработку "
            "заявок после подписания соглашения с РГП ГРС"
        ).format(num=application.application_number)

        return render(request, "applications/success.html", {
            "application": application,
            "message": message,
        })

    return redirect("index")
