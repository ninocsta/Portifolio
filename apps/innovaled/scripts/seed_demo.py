from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

APP_ROOT = Path(os.environ.get("PORTFOLIO_APP_ROOT", Path(__file__).resolve().parents[4] / "innovaled"))
sys.path.insert(0, str(APP_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from core.models import (
    Banco,
    Cliente,
    Contrato,
    DocumentoContrato,
    FormaPagamento,
    Local,
    Registro,
    StatusContrato,
    Vendedor,
    Video,
)


def main() -> None:
    DocumentoContrato.objects.all().delete()
    Video.objects.all().delete()
    Registro.objects.all().delete()
    Contrato.objects.all().delete()
    StatusContrato.objects.all().delete()
    FormaPagamento.objects.all().delete()
    Local.objects.all().delete()
    Vendedor.objects.all().delete()
    Banco.objects.all().delete()
    Cliente.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    user = User.objects.create_superuser(
        username="demo",
        password="Demo@123456",
        email="demo@portfolio.local",
        first_name="Demo",
        last_name="Portfolio",
    )

    banco_inter = Banco.objects.create(nome="Banco Inter", created_by=user, updated_by=user)
    banco_bb = Banco.objects.create(nome="Banco do Brasil", created_by=user, updated_by=user)

    vendedor_luana = Vendedor.objects.create(nome="Luana Martins", created_by=user, updated_by=user)
    vendedor_caio = Vendedor.objects.create(nome="Caio Ribeiro", created_by=user, updated_by=user)

    local_centro = Local.objects.create(nome="Painel Centro", created_by=user, updated_by=user)
    local_avenida = Local.objects.create(nome="Avenida Norte", created_by=user, updated_by=user)
    local_shopping = Local.objects.create(nome="Shopping Sul", created_by=user, updated_by=user)

    forma_boleto = FormaPagamento.objects.create(nome="Boleto", created_by=user, updated_by=user)
    forma_pix = FormaPagamento.objects.create(nome="Pix", created_by=user, updated_by=user)
    forma_cartao = FormaPagamento.objects.create(nome="Cartão", created_by=user, updated_by=user)

    status_ativo = StatusContrato.objects.create(nome_status="Ativo", created_by=user, updated_by=user)
    status_renovacao = StatusContrato.objects.create(nome_status="Renovação", created_by=user, updated_by=user)
    status_encerrado = StatusContrato.objects.create(nome_status="Encerrado", created_by=user, updated_by=user)

    clientes = [
        Cliente.objects.create(
            razao_social="Studio Horizonte Arquitetura",
            cpf_cnpj="12345678000191",
            email="horizonte@portfolio.demo",
            telefone="51990000001",
            telefone_financeiro="51990001001",
            email_financeiro="financeiro.horizonte@portfolio.demo",
            created_by=user,
            updated_by=user,
        ),
        Cliente.objects.create(
            razao_social="Clinica Aurora Vida",
            cpf_cnpj="22345678000191",
            email="aurora@portfolio.demo",
            telefone="51990000002",
            telefone_financeiro="51990001002",
            email_financeiro="financeiro.aurora@portfolio.demo",
            created_by=user,
            updated_by=user,
        ),
        Cliente.objects.create(
            razao_social="Mercado Campo Bello",
            cpf_cnpj="32345678000191",
            email="campo-bello@portfolio.demo",
            telefone="51990000003",
            telefone_financeiro="51990001003",
            email_financeiro="financeiro.campobello@portfolio.demo",
            created_by=user,
            updated_by=user,
        ),
    ]

    today = date.today()
    contratos = [
        Contrato.objects.create(
            cliente=clientes[0],
            banco=banco_inter,
            cobranca_gerada=False,
            vendedor=vendedor_luana,
            vigencia_meses=12,
            valor_mensalidade=Decimal("1290.00"),
            data_assinatura=today - timedelta(days=45),
            data_vencimento_contrato=today + timedelta(days=18),
            data_vencimento_primeira_parcela=today - timedelta(days=15),
            data_ultima_parcela=today + timedelta(days=315),
            forma_pagamento=forma_boleto,
            observacoes="Contrato focado em presença de marca em corredor urbano.",
            link_cobranca="https://portfolio.demo/cobranca/horizonte",
            link_notas="https://portfolio.demo/notas/horizonte",
            status=status_ativo,
            created_by=user,
            updated_by=user,
        ),
        Contrato.objects.create(
            cliente=clientes[1],
            banco=banco_bb,
            cobranca_gerada=True,
            vendedor=vendedor_caio,
            vigencia_meses=18,
            valor_mensalidade=Decimal("1790.00"),
            data_assinatura=today - timedelta(days=72),
            primeiro_pagamento=today - timedelta(days=40),
            segundo_pagamento=None,
            data_vencimento_contrato=today + timedelta(days=42),
            data_vencimento_primeira_parcela=today - timedelta(days=42),
            data_ultima_parcela=today + timedelta(days=468),
            forma_pagamento=forma_pix,
            observacoes="Campanha institucional com peças sazonais e apoio em shopping.",
            link_cobranca="https://portfolio.demo/cobranca/aurora",
            link_notas="https://portfolio.demo/notas/aurora",
            status=status_ativo,
            created_by=user,
            updated_by=user,
        ),
        Contrato.objects.create(
            cliente=clientes[2],
            banco=banco_inter,
            cobranca_gerada=True,
            vendedor=vendedor_luana,
            vigencia_meses=6,
            valor_mensalidade=Decimal("980.00"),
            data_assinatura=today - timedelta(days=120),
            primeiro_pagamento=today - timedelta(days=90),
            segundo_pagamento=today - timedelta(days=60),
            data_vencimento_contrato=today + timedelta(days=8),
            data_vencimento_primeira_parcela=today - timedelta(days=90),
            data_ultima_parcela=today + timedelta(days=90),
            forma_pagamento=forma_cartao,
            observacoes="Contrato de baixo ciclo com renovação em negociação.",
            link_cobranca="https://portfolio.demo/cobranca/campo-bello",
            link_notas="https://portfolio.demo/notas/campo-bello",
            status=status_renovacao,
            created_by=user,
            updated_by=user,
        ),
        Contrato.objects.create(
            cliente=clientes[0],
            banco=banco_bb,
            cobranca_gerada=True,
            vendedor=vendedor_caio,
            vigencia_meses=24,
            valor_mensalidade=Decimal("2450.00"),
            data_assinatura=today - timedelta(days=210),
            primeiro_pagamento=today - timedelta(days=180),
            segundo_pagamento=today - timedelta(days=150),
            data_vencimento_contrato=today - timedelta(days=10),
            data_cancelamento_contrato=today - timedelta(days=5),
            data_vencimento_primeira_parcela=today - timedelta(days=180),
            data_ultima_parcela=today + timedelta(days=330),
            forma_pagamento=forma_boleto,
            observacoes="Contrato encerrado e mantido para histórico operacional.",
            status=status_encerrado,
            created_by=user,
            updated_by=user,
        ),
    ]

    videos = [
        Video.objects.create(
            contrato=contratos[0],
            tempo_video=timedelta(seconds=15),
            local=local_centro,
            status=False,
            created_by=user,
            updated_by=user,
        ),
        Video.objects.create(
            contrato=contratos[1],
            tempo_video=timedelta(seconds=20),
            local=local_shopping,
            status=False,
            created_by=user,
            updated_by=user,
        ),
        Video.objects.create(
            contrato=contratos[2],
            tempo_video=timedelta(seconds=10),
            local=local_avenida,
            status=True,
            data_subiu=today - timedelta(days=7),
            created_by=user,
            updated_by=user,
        ),
    ]

    for index, contrato in enumerate(contratos[:3], start=1):
        Registro.objects.create(
            contrato=contrato,
            observacao=f"Reunião comercial #{index} concluída com alinhamento de calendário.",
            created_by=user,
            updated_by=user,
        )
        Registro.objects.create(
            contrato=contrato,
            observacao=f"Follow-up operacional do contrato {contrato.id_contrato:05d}.",
            created_by=user,
            updated_by=user,
        )

    documento = DocumentoContrato(
        contrato=contratos[1],
        descricao="Resumo comercial demo",
        created_by=user,
        updated_by=user,
    )
    documento.arquivo.save(
        "resumo-comercial-demo.txt",
        ContentFile(b"Documento ficticio para portfolio.\n"),
        save=True,
    )

    videos[2].status = True
    videos[2].save(update_fields=["status"])

    print("Seed demo de innovaled concluído para usuário demo")


if __name__ == "__main__":
    main()
