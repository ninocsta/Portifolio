#!/usr/bin/env python3
import os
import sys
from datetime import timedelta
from decimal import Decimal
from io import BytesIO
from pathlib import Path

APP_ROOT = Path(os.environ["PORTFOLIO_APP_ROOT"]).resolve()
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.development")

import django

django.setup()

from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image, ImageDraw

from billing.models import BillingPayment, BillingProfile, SaasConfig
from despesas.models import DespesaMensal, DespesaVeiculo
from lojas.models import Loja
from portal.models import FipeConsultaMetric
from portal.permissions import ensure_loja_permission_matrix
from users.models import User
from veiculos.models import Acessorio, Veiculo, VeiculoImagem


def image_bytes(label, background, size):
    image = Image.new("RGB", size, background)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, size[0] - 18, size[1] - 18), radius=28, outline="white", width=3)
    draw.text((36, size[1] // 2 - 18), label, fill="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def attach_logo(loja):
    if loja.logo:
        return
    logo_file = ContentFile(image_bytes("PM", "#1d4ed8", (320, 320)), name="portfolio-motors-logo.png")
    loja.logo.save(logo_file.name, logo_file, save=True)


def attach_vehicle_image(veiculo, label, background, order=0, is_cover=False):
    photo = VeiculoImagem.objects.create(
        loja=veiculo.loja,
        veiculo=veiculo,
        ordem=order,
        is_capa=is_cover,
    )
    file_name = f"{veiculo.slug}-{order + 1}.png"
    photo.imagem.save(
        file_name,
        ContentFile(image_bytes(label, background, (1280, 960)), name=file_name),
        save=True,
    )


def create_vehicle(loja, data, accessories, photos):
    veiculo = Veiculo.objects.create(loja=loja, **data)
    if accessories:
        veiculo.acessorios.set(accessories)
    for order, photo in enumerate(photos):
        attach_vehicle_image(
            veiculo,
            photo["label"],
            photo["background"],
            order=order,
            is_cover=order == 0,
        )
    return veiculo


today = timezone.localdate()
current_month_start = today.replace(day=1)
last_month_end = current_month_start - timedelta(days=1)
last_month_start = last_month_end.replace(day=1)
two_months_end = last_month_start - timedelta(days=1)
two_months_start = two_months_end.replace(day=1)
three_months_end = two_months_start - timedelta(days=1)
three_months_start = three_months_end.replace(day=1)

SaasConfig.objects.update_or_create(
    pk=1,
    defaults={
        "saas_plan_name": "Portfolio Motors Platform",
        "saas_plan_price": Decimal("297.00"),
        "grace_period_days": 5,
        "warning_days_before_due": 7,
    },
)

loja = Loja.objects.create(
    nome="Portfolio Motors",
    dominio="demo.localtest.me",
    subdominio="demo",
    cor_primaria="#1d4ed8",
    whatsapp="(51) 99999-0000",
    telefone="(51) 3333-0000",
    email="contato@portfolio-motors.demo",
    endereco="Av. das Garagens, 1500 - Porto Alegre/RS",
    endereco_cep="90000-000",
    endereco_logradouro="Av. das Garagens",
    endereco_numero="1500",
    endereco_bairro="Navegantes",
    endereco_cidade="Porto Alegre",
    endereco_uf="RS",
    horario_estruturado={
        "seg": {"aberto": True, "manha": {"inicio": "09:00", "fim": "12:00"}, "tarde": {"inicio": "13:30", "fim": "18:30"}},
        "ter": {"aberto": True, "manha": {"inicio": "09:00", "fim": "12:00"}, "tarde": {"inicio": "13:30", "fim": "18:30"}},
        "qua": {"aberto": True, "manha": {"inicio": "09:00", "fim": "12:00"}, "tarde": {"inicio": "13:30", "fim": "18:30"}},
        "qui": {"aberto": True, "manha": {"inicio": "09:00", "fim": "12:00"}, "tarde": {"inicio": "13:30", "fim": "18:30"}},
        "sex": {"aberto": True, "manha": {"inicio": "09:00", "fim": "12:00"}, "tarde": {"inicio": "13:30", "fim": "18:30"}},
        "sab": {"aberto": True, "inicio": "09:00", "fim": "13:00"},
        "dom": {"aberto": False},
    },
    trial_inicio=timezone.now() - timedelta(days=3),
    trial_dias=30,
)
attach_logo(loja)

User.objects.create_user(
    username="demo",
    email="demo@portfolio-motors.demo",
    password="Demo@123456",
    loja=loja,
    cargo=User.Cargo.ADMIN,
    first_name="Demo",
    last_name="Gestor",
    portal_welcome_seen=True,
    terms_accepted_at=timezone.now(),
    terms_version="portfolio-v1",
)

ensure_loja_permission_matrix(loja)

BillingProfile.objects.create(
    loja=loja,
    billing_status=BillingProfile.Status.ACTIVE,
    billing_method=BillingProfile.Method.PIX,
    next_due_date=today + timedelta(days=21),
    asaas_customer_id="cus_demo_portfolio",
    asaas_subscription_id="sub_demo_portfolio",
    asaas_last_payment_id="pay_demo_paid",
    asaas_last_payment_status="RECEIVED",
    cpf_cnpj="12345678000199",
    holder_name="Portfolio Motors Ltda",
    holder_email="financeiro@portfolio-motors.demo",
    holder_phone="51999990000",
    postal_code="90000000",
    address="Av. das Garagens",
    address_number="1500",
    province="Navegantes",
    city="Porto Alegre",
    state="RS",
)

BillingPayment.objects.create(
    loja=loja,
    asaas_payment_id="pay_demo_paid",
    billing_type="PIX",
    status="RECEIVED",
    value=Decimal("297.00"),
    due_date=today - timedelta(days=8),
    paid_at=timezone.now() - timedelta(days=7),
    invoice_url="https://example.com/invoices/pay-demo-paid",
)
BillingPayment.objects.create(
    loja=loja,
    asaas_payment_id="pay_demo_next",
    billing_type="PIX",
    status="PENDING",
    value=Decimal("297.00"),
    due_date=today + timedelta(days=21),
    invoice_url="https://example.com/invoices/pay-demo-next",
    pix_payload="000201demoportfolio",
)

acessorios = {
    "Central multimidia": Acessorio.objects.create(loja=loja, nome="Central multimidia"),
    "Camera de re": Acessorio.objects.create(loja=loja, nome="Camera de re"),
    "Bancos em couro": Acessorio.objects.create(loja=loja, nome="Bancos em couro"),
    "Piloto automatico": Acessorio.objects.create(loja=loja, nome="Piloto automatico"),
    "Sensor de estacionamento": Acessorio.objects.create(loja=loja, nome="Sensor de estacionamento"),
}

vehicles = []
vehicles.append(
    create_vehicle(
        loja,
        {
            "marca_nome": "Toyota",
            "modelo_nome": "Corolla XEi",
            "ano": today.year,
            "ano_modelo": today.year,
            "quilometragem": 18500,
            "motor": "2.0 Flex Automatico",
            "placa": "PMT1A23",
            "combustivel": Veiculo.Combustivel.FLEX,
            "cambio": Veiculo.Cambio.AUTOMATICO,
            "cor": "Branco Perolizado",
            "portas": 4,
            "categoria": Veiculo.Categoria.SEDAN,
            "valor_custo": Decimal("112000.00"),
            "valor_tabela": Decimal("134900.00"),
            "valor_venda": Decimal("129900.00"),
            "valor_sob_consulta": False,
            "publicar_no_site": True,
            "destaque": True,
            "data_entrada": today - timedelta(days=22),
            "observacoes": "Sedan com revisoes em dia, interior premium e pacote completo para vitrine principal.",
        },
        [acessorios["Central multimidia"], acessorios["Bancos em couro"], acessorios["Camera de re"]],
        [
            {"label": "Corolla XEi", "background": "#0f766e"},
            {"label": "Interior Premium", "background": "#155e75"},
        ],
    )
)
vehicles.append(
    create_vehicle(
        loja,
        {
            "marca_nome": "Jeep",
            "modelo_nome": "Compass Longitude",
            "ano": today.year - 1,
            "ano_modelo": today.year,
            "quilometragem": 32100,
            "motor": "1.3 Turbo Flex",
            "placa": "PMT4B56",
            "combustivel": Veiculo.Combustivel.FLEX,
            "cambio": Veiculo.Cambio.AUTOMATICO,
            "cor": "Cinza Grafite",
            "portas": 4,
            "categoria": Veiculo.Categoria.SUV,
            "valor_custo": Decimal("132000.00"),
            "valor_tabela": Decimal("159900.00"),
            "valor_venda": Decimal("154900.00"),
            "valor_sob_consulta": False,
            "publicar_no_site": True,
            "destaque": True,
            "data_entrada": today - timedelta(days=14),
            "observacoes": "SUV com perfil familiar e acabamento acima da media, ideal para o destaque da home.",
        },
        [acessorios["Piloto automatico"], acessorios["Sensor de estacionamento"], acessorios["Camera de re"]],
        [
            {"label": "Compass", "background": "#475569"},
            {"label": "Painel Digital", "background": "#334155"},
        ],
    )
)
vehicles.append(
    create_vehicle(
        loja,
        {
            "marca_nome": "Volkswagen",
            "modelo_nome": "Nivus Comfortline",
            "ano": today.year - 1,
            "ano_modelo": today.year - 1,
            "quilometragem": 27400,
            "motor": "200 TSI Automatico",
            "placa": "PMT7C89",
            "combustivel": Veiculo.Combustivel.FLEX,
            "cambio": Veiculo.Cambio.AUTOMATICO,
            "cor": "Azul Noturno",
            "portas": 4,
            "categoria": Veiculo.Categoria.SUV,
            "valor_custo": Decimal("98000.00"),
            "valor_tabela": Decimal("117900.00"),
            "valor_venda": Decimal("114500.00"),
            "valor_sob_consulta": False,
            "publicar_no_site": True,
            "destaque": False,
            "data_entrada": today - timedelta(days=34),
            "observacoes": "Crossover urbano com boa procura, usado para mostrar variedade do estoque.",
        },
        [acessorios["Central multimidia"], acessorios["Sensor de estacionamento"]],
        [
            {"label": "Nivus", "background": "#1e40af"},
        ],
    )
)
vehicles.append(
    create_vehicle(
        loja,
        {
            "marca_nome": "Honda",
            "modelo_nome": "City Hatch Touring",
            "ano": today.year - 2,
            "ano_modelo": today.year - 1,
            "quilometragem": 41500,
            "motor": "1.5 Flex CVT",
            "placa": "PMT0D12",
            "combustivel": Veiculo.Combustivel.FLEX,
            "cambio": Veiculo.Cambio.CVT,
            "cor": "Vermelho Mercury",
            "portas": 4,
            "categoria": Veiculo.Categoria.HATCH,
            "valor_custo": Decimal("90500.00"),
            "valor_tabela": Decimal("105900.00"),
            "valor_venda": Decimal("101900.00"),
            "valor_sob_consulta": False,
            "publicar_no_site": True,
            "destaque": False,
            "data_entrada": today - timedelta(days=46),
            "observacoes": "Hatch de maior giro para demonstrar mix de categorias na vitrine publica.",
        },
        [acessorios["Camera de re"], acessorios["Bancos em couro"]],
        [
            {"label": "City Hatch", "background": "#991b1b"},
        ],
    )
)

sold_1 = create_vehicle(
    loja,
    {
        "marca_nome": "Chevrolet",
        "modelo_nome": "Tracker Premier",
        "ano": today.year - 1,
        "ano_modelo": today.year - 1,
        "quilometragem": 29800,
        "motor": "1.2 Turbo Automatico",
        "placa": "PMT2E34",
        "combustivel": Veiculo.Combustivel.FLEX,
        "cambio": Veiculo.Cambio.AUTOMATICO,
        "cor": "Prata Switchblade",
        "portas": 4,
        "categoria": Veiculo.Categoria.SUV,
        "valor_custo": Decimal("101000.00"),
        "valor_venda": Decimal("122900.00"),
        "publicar_no_site": False,
        "destaque": False,
        "vendido": True,
        "data_entrada": today - timedelta(days=40),
        "data_venda": today - timedelta(days=4),
        "observacoes": "Unidade vendida neste mes para compor o painel financeiro.",
    },
    [acessorios["Central multimidia"], acessorios["Piloto automatico"]],
    [{"label": "Tracker Vendida", "background": "#0f766e"}],
)

sold_2 = create_vehicle(
    loja,
    {
        "marca_nome": "Fiat",
        "modelo_nome": "Toro Volcano",
        "ano": today.year - 1,
        "ano_modelo": today.year - 1,
        "quilometragem": 35200,
        "motor": "2.0 Diesel 4x4",
        "placa": "PMT5F67",
        "combustivel": Veiculo.Combustivel.DIESEL,
        "cambio": Veiculo.Cambio.AUTOMATICO,
        "cor": "Preto Carbon",
        "portas": 4,
        "categoria": Veiculo.Categoria.PICKUP,
        "valor_custo": Decimal("128000.00"),
        "valor_venda": Decimal("149900.00"),
        "publicar_no_site": False,
        "destaque": False,
        "vendido": True,
        "data_entrada": today - timedelta(days=55),
        "data_venda": today - timedelta(days=11),
        "observacoes": "Pickup vendida neste mes para reforcar margem e ticket medio.",
    },
    [acessorios["Sensor de estacionamento"], acessorios["Camera de re"]],
    [{"label": "Toro Vendida", "background": "#3f3f46"}],
)

sold_3 = create_vehicle(
    loja,
    {
        "marca_nome": "Hyundai",
        "modelo_nome": "Creta Platinum",
        "ano": today.year - 2,
        "ano_modelo": today.year - 1,
        "quilometragem": 38600,
        "motor": "1.0 Turbo Automatico",
        "placa": "PMT8G90",
        "combustivel": Veiculo.Combustivel.FLEX,
        "cambio": Veiculo.Cambio.AUTOMATICO,
        "cor": "Cinza Silk",
        "portas": 4,
        "categoria": Veiculo.Categoria.SUV,
        "valor_custo": Decimal("108000.00"),
        "valor_venda": Decimal("129500.00"),
        "publicar_no_site": False,
        "destaque": False,
        "vendido": True,
        "data_entrada": last_month_start + timedelta(days=3),
        "data_venda": last_month_start + timedelta(days=19),
        "observacoes": "Venda do mes anterior para enriquecer a serie historica do dashboard.",
    },
    [acessorios["Bancos em couro"], acessorios["Piloto automatico"]],
    [{"label": "Creta Vendida", "background": "#1d4ed8"}],
)

sold_4 = create_vehicle(
    loja,
    {
        "marca_nome": "Renault",
        "modelo_nome": "Kwid Outsider",
        "ano": today.year - 2,
        "ano_modelo": today.year - 2,
        "quilometragem": 45200,
        "motor": "1.0 Manual",
        "placa": "PMT3H21",
        "combustivel": Veiculo.Combustivel.FLEX,
        "cambio": Veiculo.Cambio.MANUAL,
        "cor": "Laranja Energy",
        "portas": 4,
        "categoria": Veiculo.Categoria.HATCH,
        "valor_custo": Decimal("45500.00"),
        "valor_venda": Decimal("57900.00"),
        "publicar_no_site": False,
        "destaque": False,
        "vendido": True,
        "data_entrada": two_months_start + timedelta(days=6),
        "data_venda": two_months_start + timedelta(days=15),
        "observacoes": "Venda de entrada para mostrar historico de faturamento.",
    },
    [acessorios["Central multimidia"]],
    [{"label": "Kwid Vendido", "background": "#ea580c"}],
)

DespesaMensal.objects.create(loja=loja, descricao="Marketing digital", valor=Decimal("1800.00"), data=today - timedelta(days=3))
DespesaMensal.objects.create(loja=loja, descricao="Aluguel do showroom", valor=Decimal("6500.00"), data=today - timedelta(days=5))
DespesaMensal.objects.create(loja=loja, descricao="Seguro da frota", valor=Decimal("2200.00"), data=last_month_start + timedelta(days=8))
DespesaMensal.objects.create(loja=loja, descricao="Fotografia automotiva", valor=Decimal("950.00"), data=three_months_start + timedelta(days=12))

DespesaVeiculo.objects.create(loja=loja, veiculo=vehicles[0], descricao="Polimento tecnico", valor=Decimal("950.00"), data=today - timedelta(days=18))
DespesaVeiculo.objects.create(loja=loja, veiculo=vehicles[1], descricao="Higienizacao premium", valor=Decimal("640.00"), data=today - timedelta(days=10))
DespesaVeiculo.objects.create(loja=loja, veiculo=sold_1, descricao="Revisao preventiva", valor=Decimal("1250.00"), data=today - timedelta(days=8))
DespesaVeiculo.objects.create(loja=loja, veiculo=sold_2, descricao="Troca de pneus", valor=Decimal("1980.00"), data=today - timedelta(days=14))
DespesaVeiculo.objects.create(loja=loja, veiculo=sold_3, descricao="Documentacao e vistoria", valor=Decimal("720.00"), data=last_month_start + timedelta(days=11))
DespesaVeiculo.objects.create(loja=loja, veiculo=sold_4, descricao="Preparacao de entrega", valor=Decimal("430.00"), data=two_months_start + timedelta(days=14))

FipeConsultaMetric.objects.create(loja=loja, total_buscas=27, ultima_busca_em=timezone.now() - timedelta(days=1))

print("Seed demo do loja_carros concluido com sucesso.")
