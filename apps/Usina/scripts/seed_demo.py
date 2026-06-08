from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

APP_ROOT = Path(os.environ.get("PORTFOLIO_APP_ROOT", Path(__file__).resolve().parents[4] / "Usina"))
sys.path.insert(0, str(APP_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()

from django.contrib.auth.models import User
from cadastros.models import (
    Cidade,
    Cliente,
    Supervisor,
    Telao,
    TipoSupervisor,
    TipoVendedor,
    Vendedor,
)
from contratos.models import Contrato, ContratoRegistro
from mensagens.models import SessaoWaha, TipoMensagem
from pagamentos.models import (
    FormaPagamento,
    LocalPagamento,
    Parcela,
    ParcelaRegistro,
    TipoPagamento,
)
from videos.models import Video


def main() -> None:
    ParcelaRegistro.objects.all().delete()
    Parcela.objects.all().delete()
    Video.objects.all().delete()
    ContratoRegistro.objects.all().delete()
    Contrato.objects.all().delete()
    TipoMensagem.objects.all().delete()
    SessaoWaha.objects.all().delete()
    Vendedor.objects.all().delete()
    Supervisor.objects.all().delete()
    Telao.objects.all().delete()
    Cidade.objects.all().delete()
    Cliente.objects.all().delete()
    FormaPagamento.objects.all().delete()
    LocalPagamento.objects.all().delete()
    TipoPagamento.objects.all().delete()
    TipoVendedor.objects.all().delete()
    TipoSupervisor.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    demo = User.objects.create_superuser(
        username="demo",
        password="Demo@123456",
        email="demo@portfolio.local",
        first_name="Demo",
        last_name="Portfolio",
    )

    supervisor_user = User.objects.create_user("supervisor.demo", password="Demo@123456", email="supervisor@portfolio.demo")
    vendedor_user_1 = User.objects.create_user("luana.vendas", password="Demo@123456", email="luana@portfolio.demo")
    vendedor_user_2 = User.objects.create_user("caio.vendas", password="Demo@123456", email="caio@portfolio.demo")

    tipo_supervisor = TipoSupervisor.objects.create(tipo="I")
    tipo_vendedor_externo = TipoVendedor.objects.create(tipo="E")
    tipo_vendedor_interno = TipoVendedor.objects.create(tipo="I")

    supervisor = Supervisor.objects.create(user=supervisor_user, tipo=tipo_supervisor, created_by=demo, updated_by=demo)
    vendedor_1 = Vendedor.objects.create(user=vendedor_user_1, supervisor=supervisor, tipo=tipo_vendedor_externo, created_by=demo, updated_by=demo)
    vendedor_2 = Vendedor.objects.create(user=vendedor_user_2, supervisor=supervisor, tipo=tipo_vendedor_interno, created_by=demo, updated_by=demo)

    porto_alegre = Cidade.objects.create(nome="Porto Alegre", created_by=demo, updated_by=demo)
    canoas = Cidade.objects.create(nome="Canoas", created_by=demo, updated_by=demo)
    novo_hamburgo = Cidade.objects.create(nome="Novo Hamburgo", created_by=demo, updated_by=demo)

    telao_centro = Telao.objects.create(nome="Telão Centro", cidade=porto_alegre, endereco="Av. Borges 100", created_by=demo, updated_by=demo)
    telao_shopping = Telao.objects.create(nome="Telão Shopping", cidade=canoas, endereco="Rua Comercial 200", created_by=demo, updated_by=demo)
    telao_avenida = Telao.objects.create(nome="Telão Avenida", cidade=novo_hamburgo, endereco="Av. Brasil 500", created_by=demo, updated_by=demo)

    cliente_1 = Cliente.objects.create(nome="Farmácia Horizonte", cpf_cnpj="12345678000101", telefone="51990000021", email="horizonte@portfolio.demo", created_by=demo, updated_by=demo)
    cliente_2 = Cliente.objects.create(nome="Clínica Vida Plena", cpf_cnpj="22345678000101", telefone="51990000022", email="vida@portfolio.demo", created_by=demo, updated_by=demo)
    cliente_3 = Cliente.objects.create(nome="Mercado Vale Sul", cpf_cnpj="32345678000101", telefone="51990000023", email="vale@portfolio.demo", created_by=demo, updated_by=demo)

    forma_boleto = FormaPagamento.objects.create(nome="Boleto")
    forma_pix = FormaPagamento.objects.create(nome="Pix")
    tipo_mensalidade = TipoPagamento.objects.create(nome="Mensalidade")
    local_cobranca = LocalPagamento.objects.create(nome="Financeiro")
    sessao_financeiro = SessaoWaha.objects.create(nome="financeiro-demo")
    TipoMensagem.objects.create(
        tipo="B",
        mensagem=(
            "Olá, {cliente_nome}! Seu contrato foi ativado para o telão {telao}, "
            "em {cidade}. Forma de pagamento: {forma_pagamento}."
        ),
        sessao=sessao_financeiro,
    )

    today = date.today()
    contrato_specs = [
        (
            telao_centro,
            dict(
            codigo_contrato="US-001",
            cliente=cliente_1,
            vendedor=vendedor_1,
            forma_pagamento=forma_boleto,
            data_assinatura_contrato=today - timedelta(days=18),
            data_primeiro_pagamento=today - timedelta(days=4),
            data_vencimento_contrato=today + timedelta(days=340),
            valor_plano=Decimal("1290.00"),
            prod_video=True,
            valor_video=Decimal("240.00"),
            forma_pagamento_video=forma_pix,
            meses=12,
            status="1",
            observacoes="Campanha de fluxo contínuo em região central.",
            created_by=demo,
            updated_by=demo,
            ),
        ),
        (
            telao_shopping,
            dict(
            codigo_contrato="US-002",
            cliente=cliente_2,
            vendedor=vendedor_2,
            forma_pagamento=forma_pix,
            data_assinatura_contrato=today - timedelta(days=47),
            data_primeiro_pagamento=today - timedelta(days=16),
            data_vencimento_contrato=today + timedelta(days=160),
            valor_plano=Decimal("1690.00"),
            prod_video=True,
            valor_video=Decimal("390.00"),
            forma_pagamento_video=forma_boleto,
            meses=18,
            status="1",
            observacoes="Contrato com revisão quinzenal de peças.",
            created_by=demo,
            updated_by=demo,
            ),
        ),
        (
            telao_avenida,
            dict(
            codigo_contrato="US-003",
            cliente=cliente_3,
            vendedor=vendedor_1,
            forma_pagamento=forma_boleto,
            data_assinatura_contrato=today - timedelta(days=83),
            data_primeiro_pagamento=today - timedelta(days=32),
            data_vencimento_contrato=today + timedelta(days=45),
            valor_plano=Decimal("980.00"),
            prod_video=False,
            valor_video=Decimal("0.00"),
            meses=6,
            status="4",
            observacoes="Contrato em fase final sem renovação definida.",
            created_by=demo,
            updated_by=demo,
            ),
        ),
    ]
    contratos = []
    for telao, payload in contrato_specs:
        contrato = Contrato(**payload)
        contrato.telao_temp = telao
        contrato.save()
        contratos.append(contrato)

    for contrato in contratos:
        ContratoRegistro.objects.create(
            contrato=contrato,
            observacoes=f"Registro operacional inicial do contrato {contrato.codigo_contrato}.",
            created_by=demo,
            updated_by=demo,
        )
        ContratoRegistro.objects.create(
            contrato=contrato,
            observacoes="Check-in de campanha e alinhamento comercial.",
            created_by=demo,
            updated_by=demo,
        )

    parcelas = [
        Parcela.objects.create(
            contrato=contratos[0],
            tipo=tipo_mensalidade,
            parcela=1,
            valor=Decimal("1290.00"),
            data_vencimento=today - timedelta(days=5),
            data_pagamento=today - timedelta(days=4),
            local=local_cobranca,
            forma=forma_boleto,
        ),
        Parcela.objects.create(
            contrato=contratos[0],
            tipo=tipo_mensalidade,
            parcela=2,
            valor=Decimal("1290.00"),
            data_vencimento=today + timedelta(days=8),
            local=local_cobranca,
            forma=forma_boleto,
        ),
        Parcela.objects.create(
            contrato=contratos[1],
            tipo=tipo_mensalidade,
            parcela=1,
            valor=Decimal("1690.00"),
            data_vencimento=today - timedelta(days=16),
            data_pagamento=today - timedelta(days=16),
            local=local_cobranca,
            forma=forma_pix,
        ),
        Parcela.objects.create(
            contrato=contratos[1],
            tipo=tipo_mensalidade,
            parcela=2,
            valor=Decimal("1690.00"),
            data_vencimento=today - timedelta(days=1),
            local=local_cobranca,
            forma=forma_pix,
            observacoes="Aguardando compensação demo",
        ),
        Parcela.objects.create(
            contrato=contratos[2],
            tipo=tipo_mensalidade,
            parcela=1,
            valor=Decimal("980.00"),
            data_vencimento=today + timedelta(days=15),
            local=local_cobranca,
            forma=forma_boleto,
        ),
    ]

    for parcela in parcelas:
        ParcelaRegistro.objects.create(
            parcela=parcela,
            observacoes=f"Histórico demo da parcela {parcela.parcela}.",
            created_by=demo,
        )

    videos = list(Video.objects.order_by("id"))
    if len(videos) >= 3:
        videos[0].status = "6"
        videos[0].updated_by = demo
        videos[0].save()
        videos[1].status = "3"
        videos[1].updated_by = demo
        videos[1].save()
        videos[2].status = "1"
        videos[2].updated_by = demo
        videos[2].save()

    print("Seed demo de Usina concluído para usuário demo")


if __name__ == "__main__":
    main()
