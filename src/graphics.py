"""Gera gráficos de barras comparando os algoritmos em cada cenário.

Execute da raiz do projeto: .venv/bin/python src/graphics.py
"""

from pathlib import Path
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


RAIZ = Path(__file__).resolve().parent.parent
PASTA_TABELAS = RAIZ / "data" / "tables"
PASTA_GRAFICOS = RAIZ / "data" / "graphics"
ALGORITMOS = {
    "insertion": ("Insertion Sort", "#e07828"),
    "merge": ("Merge Sort", "#2378ae"),
}
CENARIOS = {
    "best": "Melhor caso",
    "medium": "Caso médio",
    "worst": "Pior caso",
}


def ler_tabela(arquivo):
    """Lê médias e os dois limites do IC de 95% do CSV da tabela."""
    tabela = pd.read_csv(arquivo).set_index("Entrada")
    colunas = {"Média (s)", "Intervalo de confiança 95% (s)"}
    if not colunas.issubset(tabela.columns):
        raise ValueError(f"Colunas necessárias ausentes em {arquivo}.")
    if tabela.index.has_duplicates:
        raise ValueError(f"Entradas repetidas em {arquivo}.")

    limites = []
    for entrada, linha in tabela.iterrows():
        try:
            inferior, superior = (
                float(valor.strip())
                for valor in linha["Intervalo de confiança 95% (s)"].strip("[]").split(";")
            )
        except (AttributeError, TypeError, ValueError) as erro:
            raise ValueError(f"IC de 95% inválido em {arquivo}, entrada {entrada}.") from erro
        media = linha["Média (s)"]
        if not 0 < inferior <= media <= superior:
            raise ValueError(f"IC de 95% inconsistente em {arquivo}, entrada {entrada}.")
        limites.append((inferior, superior))

    tabela["Limite inferior"] = [par[0] for par in limites]
    tabela["Limite superior"] = [par[1] for par in limites]
    return tabela


def gerar_grafico(cenario, nome_cenario, pasta_tabelas, pasta_graficos):
    """Cria um gráfico comparativo e o salva nas duas pastas do cenário."""
    dados = {
        algoritmo: ler_tabela(pasta_tabelas / algoritmo / cenario / "tabela.csv")
        for algoritmo in ALGORITMOS
    }
    entradas = sorted(set().union(*(tabela.index for tabela in dados.values())))
    if not entradas:
        raise ValueError(f"Nenhuma entrada para o cenário {cenario}.")

    figura, eixo = plt.subplots(figsize=(18, 8.5))
    limites_inferiores = []
    limites_superiores = []
    largura = 0.38

    for indice, (algoritmo, (nome_algoritmo, cor)) in enumerate(ALGORITMOS.items()):
        tabela = dados[algoritmo]
        presentes = [(i, entrada) for i, entrada in enumerate(entradas) if entrada in tabela.index]
        posicoes = [i + (indice - 0.5) * largura for i, _ in presentes]
        medias = [tabela.at[entrada, "Média (s)"] for _, entrada in presentes]
        inferiores = [tabela.at[entrada, "Limite inferior"] for _, entrada in presentes]
        superiores = [tabela.at[entrada, "Limite superior"] for _, entrada in presentes]
        limites_inferiores.extend(inferiores)
        limites_superiores.extend(superiores)

        eixo.bar(posicoes, medias, width=largura, color=cor, label=nome_algoritmo, zorder=3)
        eixo.errorbar(
            posicoes,
            medias,
            yerr=[
                [media - inferior for media, inferior in zip(medias, inferiores)],
                [superior - media for media, superior in zip(medias, superiores)],
            ],
            fmt="none",
            ecolor="#172638",
            elinewidth=1.3,
            capsize=4,
            capthick=1.3,
            label="IC 95%" if indice == 0 else "_nolegend_",
            zorder=4,
        )

    eixo.set_yscale("log")
    eixo.set_ylim(min(limites_inferiores) / 1.8, max(limites_superiores) * 1.8)
    eixo.set_xticks(range(len(entradas)))
    eixo.set_xticklabels([f"{int(n):,}".replace(",", ".") for n in entradas])
    eixo.set_xlabel("Entrada (n)", fontsize=12)
    eixo.set_ylabel("Tempo médio de execução (s) — escala logarítmica", fontsize=12)
    eixo.set_title(f"Insertion Sort × Merge Sort — {nome_cenario}", fontsize=18, pad=20)
    itens, rotulos = eixo.get_legend_handles_labels()
    ordem = ["Insertion Sort", "Merge Sort", "IC 95%"]
    eixo.legend(
        [itens[rotulos.index(rotulo)] for rotulo in ordem],
        ordem,
        title="Algoritmo e intervalo de confiança",
        loc="upper left",
    )
    eixo.grid(axis="y", which="major", color="#d8e0e8", linewidth=0.8)
    eixo.set_axisbelow(True)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(axis="both", labelsize=10)
    figura.tight_layout()

    pastas = [pasta_graficos / algoritmo / cenario for algoritmo in ALGORITMOS]
    for pasta in pastas:
        pasta.mkdir(parents=True, exist_ok=True)
    arquivo_principal = pastas[0] / "grafico.png"
    figura.savefig(arquivo_principal, dpi=180, facecolor="white")
    plt.close(figura)
    shutil.copyfile(arquivo_principal, pastas[1] / "grafico.png")
    print(f"{nome_cenario}: {pastas[0]} e {pastas[1]}")


def gerar_graficos(pasta_tabelas=PASTA_TABELAS, pasta_graficos=PASTA_GRAFICOS):
    """Gera os três gráficos comparativos em data/graphics."""
    pasta_tabelas = Path(pasta_tabelas)
    pasta_graficos = Path(pasta_graficos)
    for cenario, nome_cenario in CENARIOS.items():
        gerar_grafico(cenario, nome_cenario, pasta_tabelas, pasta_graficos)


if __name__ == "__main__":
    gerar_graficos()
