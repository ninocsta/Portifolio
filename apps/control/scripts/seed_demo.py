from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

APP_ROOT = Path(os.environ.get("PORTFOLIO_APP_ROOT", Path(__file__).resolve().parents[4] / "control"))
sys.path.insert(0, str(APP_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from clientes.models import Cliente
from contratos.models import Contrato
from infra.backups.models import VPSBackup, VPSBackupCost
from infra.dominios.models import Dominio, DomainCost
from infra.emails.models import DomainEmail, DomainEmailCost
from infra.financeiro.models import ContratoSnapshot, DespesaAdicional, PeriodoFinanceiro
from infra.hosting.models import Hosting, HostingCost
from infra.vps.models import VPS, VPSContrato, VPSCost
from invoices.models import Invoice, InvoiceContrato, MessageQueue


def main() -> None:
    MessageQueue.objects.all().delete()
    InvoiceContrato.objects.all().delete()
    Invoice.objects.all().delete()
    ContratoSnapshot.objects.all().delete()
    DespesaAdicional.objects.all().delete()
    PeriodoFinanceiro.objects.all().delete()
    DomainEmailCost.objects.all().delete()
    DomainEmail.objects.all().delete()
    VPSBackupCost.objects.all().delete()
    VPSBackup.objects.all().delete()
    VPSCost.objects.all().delete()
    VPSContrato.objects.all().delete()
    VPS.objects.all().delete()
    HostingCost.objects.all().delete()
    Hosting.objects.all().delete()
    DomainCost.objects.all().delete()
    Dominio.objects.all().delete()
    Contrato.objects.all().delete()
    Cliente.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    user = User.objects.create_superuser(
        username="demo",
        password="Demo@123456",
        email="demo@portfolio.local",
        first_name="Demo",
        last_name="Portfolio",
    )

    today = date.today()
    current_month_start = today.replace(day=1)
    previous_month_start = (current_month_start - timedelta(days=1)).replace(day=1)

    clientes = [
        Cliente.objects.create(
            nome="Costa Studio Digital",
            email="contato.costa@portfolio.demo",
            telefone="51990000011",
            tipo="pessoa_juridica",
            vencimento_padrao=5,
            descricao_cobranca="Retainer mensal de produto e infraestrutura",
        ),
        Cliente.objects.create(
            nome="Atlas Consultoria Fiscal",
            email="atlas@portfolio.demo",
            telefone="51990000012",
            tipo="pessoa_juridica",
            vencimento_padrao=10,
            descricao_cobranca="Sustentação e operação recorrente",
        ),
        Cliente.objects.create(
            nome="Operação Interna",
            email="interno@portfolio.demo",
            telefone="51990000013",
            tipo="interno",
            vencimento_padrao=15,
            descricao_cobranca="Custos internos",
        ),
    ]

    contratos = [
        Contrato.objects.create(
            cliente=clientes[0],
            nome="Portal institucional",
            descricao="Contrato principal de desenvolvimento e sustentação.",
            valor_mensal=Decimal("3200.00"),
            data_inicio=previous_month_start - timedelta(days=120),
        ),
        Contrato.objects.create(
            cliente=clientes[1],
            nome="ERP sob medida",
            descricao="Sustentação e pequenas entregas contínuas.",
            valor_mensal=Decimal("4600.00"),
            data_inicio=previous_month_start - timedelta(days=210),
        ),
        Contrato.objects.create(
            cliente=clientes[2],
            nome="Ferramentas internas",
            descricao="Contrato interno sem faturamento externo.",
            valor_mensal=Decimal("0.00"),
            data_inicio=previous_month_start - timedelta(days=360),
        ),
    ]

    dominio = Dominio.objects.create(nome="costastudio.app", fornecedor="RegistroBR", ativo=True)
    dominio.contratos.set([contratos[0]])
    DomainCost.objects.create(
        domain=dominio,
        valor_total=Decimal("180.00"),
        periodo_meses=12,
        data_inicio=previous_month_start - timedelta(days=200),
        vencimento=today + timedelta(days=9),
        ativo=True,
    )

    hosting = Hosting.objects.create(nome="App Shared Cloud", fornecedor="Hostinger", ativo=True)
    hosting.contratos.set([contratos[0], contratos[1]])
    HostingCost.objects.create(
        hosting=hosting,
        valor_total=Decimal("420.00"),
        periodo_meses=1,
        data_inicio=current_month_start,
        vencimento=today + timedelta(days=15),
        ativo=True,
    )

    vps = VPS.objects.create(nome="API Node 02", fornecedor="Hetzner", ativo=True)
    VPSContrato.objects.create(
        vps=vps,
        contrato=contratos[1],
        data_inicio=previous_month_start - timedelta(days=90),
        ativo=True,
    )
    VPSCost.objects.create(
        vps=vps,
        valor_total=Decimal("600.00"),
        periodo_meses=1,
        data_inicio=current_month_start,
        vencimento=today + timedelta(days=6),
        ativo=True,
    )

    backup = VPSBackup.objects.create(vps=vps, nome="Snapshot diário", fornecedor="Hetzner", ativo=True)
    VPSBackupCost.objects.create(
        backup=backup,
        valor_total=Decimal("90.00"),
        periodo_meses=1,
        data_inicio=current_month_start,
        vencimento=today + timedelta(days=6),
        ativo=True,
    )

    email_service = DomainEmail.objects.create(
        dominio=dominio,
        contrato=contratos[0],
        fornecedor="Google Workspace",
        quantidade_caixas=5,
        ativo=True,
    )
    DomainEmailCost.objects.create(
        email=email_service,
        valor_total=Decimal("140.00"),
        periodo_meses=1,
        data_inicio=current_month_start,
        vencimento=today + timedelta(days=12),
        ativo=True,
    )

    periodo_fechado = PeriodoFinanceiro.objects.create(
        mes=previous_month_start.month,
        ano=previous_month_start.year,
        fechado=True,
        fechado_em=timezone.now() - timedelta(days=20),
        fechado_por=user.username,
        observacoes="Fechamento demo do portfolio.",
    )

    snapshot_specs = [
        (contratos[0], Decimal("3200.00"), Decimal("15.00"), Decimal("210.00"), Decimal("0.00"), Decimal("0.00"), Decimal("140.00"), Decimal("80.00")),
        (contratos[1], Decimal("4600.00"), Decimal("0.00"), Decimal("210.00"), Decimal("600.00"), Decimal("90.00"), Decimal("0.00"), Decimal("150.00")),
        (contratos[2], Decimal("0.00"), Decimal("0.00"), Decimal("0.00"), Decimal("180.00"), Decimal("0.00"), Decimal("0.00"), Decimal("60.00")),
    ]
    for contrato, receita, dominios, hostings, vps_cost, backups, emails, extras in snapshot_specs:
        custo_total = dominios + hostings + vps_cost + backups + emails + extras
        margem = receita - custo_total
        margem_percentual = (margem / receita * 100) if receita > 0 else None
        ContratoSnapshot.objects.create(
            contrato=contrato,
            periodo=periodo_fechado,
            receita=receita,
            custo_dominios=dominios,
            custo_hostings=hostings,
            custo_vps=vps_cost,
            custo_backups=backups,
            custo_emails=emails,
            custo_despesas_adicionais=extras,
            custo_total=custo_total,
            margem=margem,
            margem_percentual=margem_percentual,
            detalhamento={"demo": True, "cliente": contrato.cliente.nome},
        )

    DespesaAdicional.objects.create(
        contrato=contratos[1],
        descricao="Horas extras de implantação",
        valor=Decimal("150.00"),
        mes_referencia=current_month_start.month,
        ano_referencia=current_month_start.year,
        observacoes="Despesa fictícia para dashboard",
        criado_por=user.username,
    )

    invoice_specs = [
        (contratos[0], clientes[0], Decimal("3200.00"), "pago", today - timedelta(days=4), "https://checkout.portfolio.demo/invoice-1"),
        (contratos[1], clientes[1], Decimal("4600.00"), "pendente", today + timedelta(days=3), "https://checkout.portfolio.demo/invoice-2"),
        (contratos[1], clientes[1], Decimal("780.00"), "atrasado", today - timedelta(days=12), "https://checkout.portfolio.demo/invoice-3"),
        (contratos[2], clientes[2], Decimal("0.00"), "cancelado", today - timedelta(days=1), ""),
    ]
    invoices = []
    for index, (contrato, cliente, valor, status, vencimento, checkout_url) in enumerate(invoice_specs, start=1):
        invoice = Invoice.objects.create(
            cliente=cliente,
            mes_referencia=current_month_start.month,
            ano_referencia=current_month_start.year,
            valor_total=valor,
            descricao=f"Cobrança demo #{index}",
            status=status,
            vencimento=vencimento,
            invoice_slug=f"portfolio-invoice-{index}",
            checkout_url=checkout_url,
            order_nsu=f"ORDER-{index:04d}",
            transaction_nsu=f"TX-{index:04d}" if status == "pago" else "",
            receipt_url=f"https://receipts.portfolio.demo/{index}" if status == "pago" else "",
            pago_em=timezone.now() - timedelta(days=2) if status == "pago" else None,
        )
        invoices.append(invoice)
        InvoiceContrato.objects.create(invoice=invoice, contrato=contrato, valor=valor)

    MessageQueue.objects.create(
        invoice=invoices[1],
        telefone="51990000012",
        mensagem="Lembrete de vencimento em 3 dias.",
        tipo="2_dias",
        agendado_para=timezone.now() + timedelta(hours=2),
        status="pendente",
    )
    MessageQueue.objects.create(
        invoice=invoices[2],
        telefone="51990000012",
        mensagem="Cobrança em atraso enviada ao financeiro.",
        tipo="atraso",
        agendado_para=timezone.now() - timedelta(days=1),
        status="enviado",
        enviado_em=timezone.now() - timedelta(hours=22),
    )

    print("Seed demo de control concluído para usuário demo")


if __name__ == "__main__":
    main()
