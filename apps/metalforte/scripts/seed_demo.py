from __future__ import annotations

import os
import sys
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

APP_ROOT = Path(os.environ.get("PORTFOLIO_APP_ROOT", Path(__file__).resolve().parents[4] / "metalforte"))
sys.path.insert(0, str(APP_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from main.models import (
    Bobina,
    Cliente,
    Espessura,
    EstoqueEPS,
    Formato,
    ItemParafuso,
    ItemPedido,
    MovimentoBobina,
    MovimentoEPS,
    MovimentoParafuso,
    Orcamento,
    Parafuso,
    Pedido,
    Produto,
)


def main() -> None:
    MovimentoParafuso.objects.all().delete()
    MovimentoEPS.objects.all().delete()
    MovimentoBobina.objects.all().delete()
    ItemParafuso.objects.all().delete()
    ItemPedido.objects.all().delete()
    Orcamento.objects.all().delete()
    Pedido.objects.all().delete()
    Espessura.objects.all().delete()
    Formato.objects.all().delete()
    EstoqueEPS.objects.all().delete()
    Bobina.objects.all().delete()
    Parafuso.objects.all().delete()
    Produto.objects.all().delete()
    Cliente.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    user = User.objects.create_superuser(
        username="demo",
        password="Demo@123456",
        email="demo@portfolio.local",
    )

    clientes = [
        Cliente.objects.create(nome="Aurora Construções", cidade="Porto Alegre", telefone="550000000001", email="aurora@portfolio.demo"),
        Cliente.objects.create(nome="Verde Campo Agro", cidade="Canoas", telefone="550000000002", email="verde@portfolio.demo"),
        Cliente.objects.create(nome="Nova Rota Logística", cidade="São Leopoldo", telefone="550000000003", email="rota@portfolio.demo"),
    ]

    produtos = [Produto.objects.create(nome=nome) for nome in ["Telha TP40", "Painel TR25", "Rufo Lateral"]]
    formatos = [
        Formato.objects.create(descricao="1,00m", largura=1000),
        Formato.objects.create(descricao="1,20m", largura=1200),
    ]

    bobina_a = Bobina.objects.create(nome="Bobina Azul", saldo_kg=Decimal("1850"), custo_kg_atual=Decimal("8.60"), peso_kg_m2=Decimal("4.20"))
    bobina_b = Bobina.objects.create(nome="Bobina Branca", saldo_kg=Decimal("1260"), custo_kg_atual=Decimal("7.95"), peso_kg_m2=Decimal("3.80"))
    eps = EstoqueEPS.objects.create(nome="EPS Densidade 18", saldo_m=Decimal("980"), custo_m_atual=Decimal("6.10"))
    parafuso = Parafuso.objects.create(descricao="Parafuso autobrocante 5/16", saldo_qtd=Decimal("8500"), custo_unitario_atual=Decimal("0.48"), valor_venda_unit=Decimal("0.95"))

    espessuras = [
        Espessura.objects.create(produto=produtos[0], espessura="30mm", preco_cliente=Decimal("98.00"), bobina_1=bobina_a, eps=eps, peso_nucleo_kg_m=Decimal("0.70"), consumo_eps_m_por_m=Decimal("1.00")),
        Espessura.objects.create(produto=produtos[1], espessura="50mm", preco_cliente=Decimal("135.00"), bobina_1=bobina_b, eps=eps, peso_nucleo_kg_m=Decimal("0.95"), consumo_eps_m_por_m=Decimal("1.00")),
    ]

    hoje = timezone.now()

    pedido_specs = [
        (clientes[0], "P", Decimal("120"), Decimal("0"), True),
        (clientes[1], "E", Decimal("180"), Decimal("45"), False),
        (clientes[2], "C", Decimal("220"), Decimal("25"), True),
    ]

    for index, (cliente, status, frete, desconto, pago) in enumerate(pedido_specs, start=1):
        pedido = Pedido.objects.create(cliente=cliente, status=status, frete=frete, desconto=desconto, pago=pago, observacoes=f"Lote {index} com prioridade comercial")
        item = ItemPedido.objects.create(
            pedido=pedido,
            produto=produtos[index % len(produtos)],
            espessura=espessuras[index % len(espessuras)],
            formato=formatos[index % len(formatos)],
            quantidade=10 + (index * 2),
            comprimento=Decimal("6000"),
        )
        ItemParafuso.objects.create(pedido=pedido, parafuso=parafuso, quantidade=120 + (index * 30))
        pedido.data_pedido = hoje - timedelta(days=index * 6)
        pedido.save(update_fields=["data_pedido"])
        if status == "C":
            pedido.estoque_baixado_em = hoje - timedelta(days=2)
            pedido.save(update_fields=["estoque_baixado_em"])

    orc_specs = [
        (clientes[0], "P"),
        (clientes[1], "A"),
        (clientes[2], "R"),
    ]
    for index, (cliente, status) in enumerate(orc_specs, start=1):
        orc = Orcamento.objects.create(cliente=cliente, status=status, frete=Decimal("90"), desconto=Decimal("15"), observacoes=f"Proposta comercial {index}")
        ItemPedido.objects.create(
            orcamento=orc,
            produto=produtos[(index + 1) % len(produtos)],
            espessura=espessuras[(index + 1) % len(espessuras)],
            formato=formatos[(index + 1) % len(formatos)],
            quantidade=8 + index,
            comprimento=Decimal("5500"),
        )
        ItemParafuso.objects.create(orcamento=orc, parafuso=parafuso, quantidade=80 + (index * 20))
        orc.data_orcamento = hoje - timedelta(days=index * 4)
        if status == "A":
            orc.data_aprovacao = hoje - timedelta(days=1)
        orc.save(update_fields=["data_orcamento", "data_aprovacao"])

    MovimentoBobina.objects.create(bobina=bobina_a, tipo="ENTRADA", quantidade_kg=Decimal("500"), custo_kg=Decimal("8.60"), valor_custo=Decimal("4300"), saldo_apos=bobina_a.saldo_kg, observacao="Reposição demo")
    MovimentoBobina.objects.create(bobina=bobina_b, tipo="SAIDA", quantidade_kg=Decimal("120"), custo_kg=Decimal("7.95"), valor_custo=Decimal("954"), saldo_apos=Decimal("1140"), observacao="Consumo produção")
    MovimentoEPS.objects.create(eps=eps, tipo="ENTRADA", quantidade_m=Decimal("300"), custo_m=Decimal("6.10"), valor_custo=Decimal("1830"), saldo_apos=eps.saldo_m, observacao="Compra demo")
    MovimentoParafuso.objects.create(parafuso=parafuso, tipo="SAIDA", quantidade=Decimal("450"), custo_unitario=Decimal("0.48"), valor_custo=Decimal("216"), saldo_apos=Decimal("8050"), observacao="Aplicação em pedidos")

    print(f"Seed demo de metalforte concluído para usuário {user.username}")


if __name__ == "__main__":
    main()
