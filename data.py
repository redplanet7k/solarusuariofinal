"""data.py — Constantes e funções base — Atlas INPE/LABREN 2017
Calibrado com dados reais de mercado MT (Jul/2026)
"""
import numpy as np

LATITUDE  = -13.05; LONGITUDE = -55.91; ALTITUDE = 384
CIDADE    = "Lucas do Rio Verde / MT"
MESES     = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
DIAS_POR_MES = [31,28,31,30,31,30,31,31,30,31,30,31]

# ── Performance do sistema ───────────────────────────────────────────
PERDA_INVERSOR=0.030; PERDA_CABEAMENTO=0.015; PERDA_SOMBREAMENTO=0.025
PERDA_SUJEIRA=0.020;  MODULO_COEF_TEMP=-0.0035; TEMP_REFERENCIA=25; TEMP_OPERACAO_LOCAL=45
PERDA_TEMPERATURA = abs(MODULO_COEF_TEMP)*(TEMP_OPERACAO_LOCAL-TEMP_REFERENCIA)
FATOR_DESEMPENHO  = round(1-(PERDA_INVERSOR+PERDA_CABEAMENTO+PERDA_SOMBREAMENTO+
                             PERDA_SUJEIRA+PERDA_TEMPERATURA),4)

# ── Módulos disponíveis no mercado MT (2025/2026) ───────────────────
# Padrão atual do mercado MT: módulos de alta potência (550-820W)
# Apollo Energy Solar usa 820Wp | Cerrado Energy usa 620Wp
# Usamos 550Wp como base conservadora (mais comum em residencial pequeno)
# e 820Wp como opção de alta potência (menor área necessária)
MODULO_POTENCIA_WP = 550    # residencial padrão (entrada)
MODULO_AREA_M2     = 2.56   # área por módulo 550Wp
MODULO_820_WP      = 820    # alta potência (Apollo/comercial)
MODULO_820_AREA    = 3.20   # área estimada por módulo 820Wp

# ── Tarifa e impostos ────────────────────────────────────────────────
TARIFA_ENERGIA_KWH       = 0.87
TARIFA_BASE_SEM_TRIBUTOS = 0.899420
TARIFA_COM_TRIBUTOS      = 1.194080
ALIQ_PIS_PASEP           = 0.0165
ALIQ_COFINS              = 0.0760
ALIQ_ICMS_MT             = 0.17
CUSTO_ILUMINACAO_PUBLICA = 22.06

# ── Parâmetros financeiros ───────────────────────────────────────────
INFLACAO_ENERGIA_AA  = 0.065   # inflação histórica energia elétrica BR
TAXA_DESCONTO        = 0.12    # custo de oportunidade (Selic referência)
VIDA_UTIL_ANOS       = 25
TAXA_DEPRECIACAO_AA  = 0.005   # 0,5% ao ano de degradação dos painéis
CUSTO_MANUTENCAO_AA  = 400.0
FATOR_EMISSAO_CO2_KG_KWH = 0.0884

# ── Taxas de financiamento reais observadas no mercado MT ───────────
# Fonte: Apollo Energy Solar, Cerrado Energy, BC4 Energia, Timas/WEG (Jul/2026)
FINANCIAMENTO_OPCOES = {
    "Apollo 60x (~1,80% a.m.)": {
        "taxa_am": 0.0180, "prazo_meses": 60,
        "descricao": "Apollo Energy Solar — Lucas do Rio Verde/MT",
        "entrada_pct": 0.0,   # sem entrada informada
    },
    "WEG/Timas 120x (~1,79% a.m.)": {
        "taxa_am": 0.0179, "prazo_meses": 120,
        "descricao": "Timas Engenharia & WEG Financiamento Solar",
        "entrada_pct": 0.0,
    },
    "Cerrado Energy 60x (2,46% a.m.)": {
        "taxa_am": 0.0246, "prazo_meses": 60,
        "descricao": "Cerrado Energy — Financiamento com 4 meses carência",
        "entrada_pct": 0.0,
    },
    "BC4 Troca Inteligente 60x (~1,50% a.m.)": {
        "taxa_am": 0.0150, "prazo_meses": 60,
        "descricao": "BC4 Energia — Troca conta de energia por parcela solar",
        "entrada_pct": 0.0,
    },
    "Banco/CDC 48x (~1,99% a.m.)": {
        "taxa_am": 0.0199, "prazo_meses": 48,
        "descricao": "Financiamento bancário padrão (CDC)",
        "entrada_pct": 0.20,  # 20% entrada típica
    },
    "À vista": {
        "taxa_am": 0.0, "prazo_meses": 0,
        "descricao": "Pagamento à vista — sem juros",
        "entrada_pct": 1.0,
    },
}

# ── Modelo de custo calibrado — mercado MT (Jul/2026) ───────────────
#
# FONTES REAIS UTILIZADAS:
#
# Apollo Energy Solar (Lucas do Rio Verde/MT — COM instalação completa):
#   Módulos 820Wp. Preço à vista estimado descontando financiamento 60x a 1,80% a.m.
#   8,20 kWp  → à vista ~R$ 21.831  → R$ 2.662/kWp
#   10,66 kWp → à vista ~R$ 27.088  → R$ 2.541/kWp
#   13,94 kWp → à vista ~R$ 33.331  → R$ 2.391/kWp
#   17,22 kWp → à vista ~R$ 42.093  → R$ 2.444/kWp
#   21,32 kWp → à vista ~R$ 49.613  → R$ 2.327/kWp
#
# Cerrado Energy (COM instalação estimada +R$2.500):
#   6,20 kWp  → R$ 15.999  → R$ 2.580/kWp
#
# BC4 Energia Troca Inteligente (preço embutido na parcela, 60x ~1,5% a.m.):
#   8,01 kWp  → à vista ~R$ 31.701  → R$ 3.956/kWp  (inclui serviços extras)
#   9,62 kWp  → à vista ~R$ 35.994  → R$ 3.743/kWp
#   12,82 kWp → à vista ~R$ 46.587  → R$ 3.634/kWp
#
# Timas Engenharia (financiamento 120x WEG ~1,79% a.m.):
#   Sistemas 3–12 kWp → R$ 2.989 a R$ 4.453/kWp à vista estimado
#
# Segmentos do mercado MT:
#   < 3 kWp  : mercado informal/sem instalação  → ~R$ 5.500–4.200/kWp
#   3–6 kWp  : residencial pequeno (entrada)    → ~R$ 4.200–3.300/kWp
#   6–10 kWp : residencial médio/standard       → ~R$ 3.300–2.660/kWp
#   10–20 kWp: residencial grande/comercial     → ~R$ 2.660–2.330/kWp
#   > 20 kWp : comercial/industrial             → ~R$ 2.330–2.000/kWp
#
# Nota: Valores referência COM instalação completa (mão de obra, estrutura,
# cabeamento, inversor e projeto elétrico). Preços variam ±15% por região do MT.

_KWP_PONTOS   = [1.0,  2.0,  3.0,  4.0,  5.0,  6.2,  8.2,   10.66, 13.94, 17.22, 21.32, 30.0]
_CUSTO_PONTOS = [5500, 4800, 4200, 3800, 3500, 3200, 2662,  2541,  2391,  2444,  2327,  2100]

def custo_por_kwp(kwp: float) -> float:
    """Retorna o custo por kWp (R$/kWp) para o sistema COM instalação,
    interpolado a partir de dados reais de mercado MT (Jul/2026)."""
    return float(np.interp(kwp, _KWP_PONTOS, _CUSTO_PONTOS))

def custo_total_sistema(kwp: float) -> float:
    """Custo total estimado do sistema instalado (R$)."""
    return round(kwp * custo_por_kwp(kwp), 2)

def faixa_custo_kwp(kwp: float) -> tuple:
    """Retorna faixa de preço (mín, med, máx) com variação regional ±15%."""
    med = custo_por_kwp(kwp)
    return (round(med * 0.85), round(med), round(med * 1.15))

def pmt(pv: float, taxa: float, n: int) -> float:
    """Calcula parcela mensal de financiamento (PMT)."""
    if taxa == 0 or n == 0:
        return pv / n if n > 0 else pv
    return round(pv * taxa / (1 - (1 + taxa) ** -n), 2)

# Mantido para compatibilidade com versões anteriores
CUSTO_POR_KWP = 3500  # referência média mercado MT 2026
