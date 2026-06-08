from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from pathlib import Path

APP_ROOT = Path(os.environ.get("PORTFOLIO_APP_ROOT", Path(__file__).resolve().parents[4] / "messages"))
sys.path.insert(0, str(APP_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()

from django.contrib.auth.models import Permission, User
from django.utils import timezone
from birthday_messages.models import Contact, Message, ModelMessage, Profile


def main() -> None:
    Message.objects.all().delete()
    ModelMessage.objects.all().delete()
    Contact.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    user = User.objects.create_user(
        username="demo",
        password="Demo@123456",
        email="demo@portfolio.local",
        first_name="Demo",
        last_name="Portfolio",
    )

    perms = Permission.objects.filter(content_type__app_label="birthday_messages")
    user.user_permissions.set(perms)

    profile, _ = Profile.objects.update_or_create(
        user=user,
        defaults={
            "email": "demo@portfolio.local",
            "phone": "550000000001",
            "connected": True,
            "last_status": "WORKING",
            "session": "portfolio-demo",
        },
    )

    model_message = ModelMessage.objects.create(
        user=user,
        message=(
            "Ola, {nome}!\n\n"
            "Passando para desejar um aniversario especial, com muita saude, prosperidade e conquistas.\n"
            "Que o novo ciclo venha com bons encontros e muitos motivos para celebrar."
        ),
    )

    names = [
        ("Mariana Alves", "Porto Alegre", "Gestora Comercial"),
        ("Rafael Martins", "Canoas", "Designer"),
        ("Camila Rocha", "São Leopoldo", "Nutricionista"),
        ("Felipe Andrade", "Novo Hamburgo", "Analista Financeiro"),
        ("Juliana Costa", "Gravataí", "Coordenadora de RH"),
        ("Bianca Nunes", "Pelotas", "Dentista"),
        ("Thiago Barros", "Passo Fundo", "Engenheiro"),
        ("Patricia Prado", "Santa Maria", "Arquiteta"),
        ("Leticia Moura", "Caxias do Sul", "Psicóloga"),
        ("Enzo Gabriel", "Lajeado", "Empreendedor"),
    ]

    today = timezone.localdate()
    contacts = []
    for index, (name, city, profession) in enumerate(names, start=1):
        birthday = today - timedelta(days=(index * 9))
        contact = Contact.objects.create(
            user=user,
            first_name=name,
            phone=f"550000000{index:03d}",
            birthday=date(1990 + (index % 8), birthday.month, min(birthday.day, 28)),
            email=f"contato{index}@portfolio.demo",
            city=city,
            profession=profession,
        )
        contacts.append(contact)

    statuses = ["Q", "S", "D", "R", "F"]
    for index, contact in enumerate(contacts, start=1):
        sent_at = timezone.now() - timedelta(days=index)
        status = statuses[index % len(statuses)]
        delivered_at = sent_at + timedelta(minutes=15) if status in {"D", "R"} else None
        Message.objects.create(
            user=user,
            contact=contact,
            message=model_message,
            message_sent=f"Mensagem enviada para {contact.first_name}",
            birthday_reference_date=today - timedelta(days=index),
            api_message_id=f"demo-message-{index}",
            status=status,
            sent_at=sent_at,
            delivered_at=delivered_at,
            error="Falha de rede simulada" if status == "F" else "",
        )

    profile.connected = True
    profile.save(update_fields=["connected"])
    print("Seed demo de messages concluído")


if __name__ == "__main__":
    main()
