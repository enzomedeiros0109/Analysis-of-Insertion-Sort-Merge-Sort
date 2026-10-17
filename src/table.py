"""Gera tabelas estatisticas dos benchmarks de Insertion Sort e Merge Sort.

Execute da raiz do projeto: .venv/bin/python src/table.py
Dependencias: .venv/bin/python -m pip install -r requirements.txt
"""

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
from scipy.stats import t


RAIZ = Path(__file__).resolve().parent.parent
ALGORITMOS = {"insertion": "Insertion Sort", "merge": "Merge Sort"}
CENARIOS = {
    "best_case": "Melhor caso",
    "medium_case": "Caso medio",
    "worst_case": "Pior caso",
}
MEDICOES_ESPERADAS = 50
TITULO_IC = "Intervalo de Confiança 95% (s)"
CABECALHOS = [
    ("Entrada", ""), ("Média (s)", ""), ("Desvio padrão (s)", ""),
    (TITULO_IC, "inferior"), (TITULO_IC, "superior"),
    ("Mínimo (s)", ""), ("Máximo (s)", ""),
]


def ler_medicoes(arquivo):
    """Le duas colunas numericas, removendo os cabecalhos repetidos."""
    try:
        dados = pd.read_csv(
            arquivo,
            header=None,
            names=["n", "tempo_s"],
            dtype=str,
            skipinitialspace=True,
            encoding="utf-8-sig",
        )
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["n", "tempo_s"])

    cabecalhos = dados["n"].str.strip().str.lower().str.startswith("entrada", na=False)
    dados = dados.loc[~cabecalhos].copy()
    dados["n"] = pd.to_numeric(dados["n"], errors="raise")
    dados["tempo_s"] = pd.to_numeric(dados["tempo_s"], errors="raise")

    # Uma linha truncada ou invalida nao deve entrar nas estatisticas.
    n_valido = (dados["n"] > 0) & (dados["n"] % 1 == 0)
    tempo_valido = (dados["tempo_s"] >= 0) & (dados["tempo_s"] < float("inf"))
    if not (n_valido & tempo_valido).all():
        raise ValueError(f"{arquivo}: entrada ou tempo invalido em uma medicao.")

    dados["n"] = dados["n"].astype("int64")
    return dados


def calcular_estatisticas(dados):
    """Calcula desvio amostral (ddof=1) e IC de 95% para a media."""
    tabela = dados.groupby("n", sort=True)["tempo_s"].agg(
        Medicoes="count",
        Media="mean",
        Desvio="std",
        Minimo="min",
        Maximo="max",
    ).reset_index()

    # IC = media +/- t(0.975, k - 1) * desvio / sqrt(k).
    # Com apenas uma medicao, o desvio e os limites ficam sem valor (NaN).
    margem = (
        t.ppf(0.975, tabela["Medicoes"] - 1)
        * tabela["Desvio"]
        / tabela["Medicoes"].pow(0.5)
    )
    tabela["inferior"] = tabela["Media"] - margem
    tabela["superior"] = tabela["Media"] + margem
    tabela = tabela.rename(columns={
        "n": "Entrada",
        "Media": "Média (s)",
        "Desvio": "Desvio padrão (s)",
        "Minimo": "Mínimo (s)",
        "Maximo": "Máximo (s)",
    })
    return tabela[[
        "Entrada", "Média (s)", "Desvio padrão (s)",
        "inferior", "superior", "Mínimo (s)", "Máximo (s)",
    ]]


def salvar_imagem(tabela, arquivo, nome_algoritmo, nome_cenario):
    """Renderiza um cabeçalho de dois níveis, agrupando os limites do IC."""
    linhas = []
    for _, linha in tabela.iterrows():
        linhas.append([
            f"{int(linha['Entrada']):,}".replace(",", "."),
            *(
                "—" if pd.isna(linha[coluna]) else f"{linha[coluna]:.8g}"
                for coluna in tabela.columns[1:]
            ),
        ])

    altura = max(4.8, 1.25 + 0.45 * (len(linhas) + 2))
    figura, eixo = plt.subplots(figsize=(16, altura))
    figura.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.87)
    eixo.axis("off")
    figura.text(
        0.5, 0.94, f"{nome_algoritmo} — {nome_cenario}",
        ha="center", va="center", fontsize=19, fontweight="bold", color="#18334f",
    )
    larguras = [0.10, 0.14, 0.16, 0.15, 0.15, 0.15, 0.15]
    posicoes = [0]
    for largura in larguras:
        posicoes.append(posicoes[-1] + largura)
    altura_linha = 1 / (len(linhas) + 2)

    def desenhar_celula(coluna, y, largura, altura, texto, cor, cabecalho=False):
        x = posicoes[coluna]
        eixo.add_patch(Rectangle(
            (x, y), largura, altura,
            facecolor=cor, edgecolor="#d3dce5", linewidth=0.7,
            transform=eixo.transAxes, clip_on=False,
        ))
        eixo.text(
            x + largura / 2, y + altura / 2, texto,
            ha="center", va="center", fontsize=11.5,
            color="white" if cabecalho else "#172638",
            fontweight="bold" if cabecalho else "normal",
            transform=eixo.transAxes,
        )

    # Os outros títulos ocupam as duas linhas de cabeçalho.
    for coluna in (0, 1, 2, 5, 6):
        desenhar_celula(
            coluna, 1 - 2 * altura_linha, larguras[coluna], 2 * altura_linha,
            CABECALHOS[coluna][0], "#183b59", cabecalho=True,
        )
    desenhar_celula(
        3, 1 - altura_linha, larguras[3] + larguras[4], altura_linha,
        TITULO_IC, "#183b59", cabecalho=True,
    )
    for coluna in (3, 4):
        desenhar_celula(
            coluna, 1 - 2 * altura_linha, larguras[coluna], altura_linha,
            CABECALHOS[coluna][1], "#183b59", cabecalho=True,
        )
    for indice, linha in enumerate(linhas):
        cor = "#ffffff" if indice % 2 == 0 else "#f4f7fa"
        for coluna, texto in enumerate(linha):
            desenhar_celula(
                coluna, 1 - (indice + 3) * altura_linha,
                larguras[coluna], altura_linha, texto, cor,
            )
    figura.savefig(arquivo, dpi=180, facecolor="white")
    plt.close(figura)


def gerar_tabelas(pasta_dados=RAIZ / "data", pasta_saida=RAIZ / "data" / "tables"):
    """Salva um CSV e um PNG em algoritmo/cenario para cada benchmark."""
    pasta_dados = Path(pasta_dados)
    pasta_saida = Path(pasta_saida)
    tabelas = []

    for algoritmo, nome_algoritmo in ALGORITMOS.items():
        for cenario, nome_cenario in CENARIOS.items():
            arquivo = pasta_dados / algoritmo / f"benchmark_{algoritmo}_{cenario}.csv"
            if not arquivo.is_file():
                print(f"Aviso: arquivo ausente: {arquivo}", file=sys.stderr)
                continue

            dados = ler_medicoes(arquivo)
            if dados.empty:
                print(f"Aviso: arquivo sem medicoes: {arquivo}", file=sys.stderr)
                continue

            tabela = calcular_estatisticas(dados)
            contagens = dados.groupby("n", sort=True).size()
            incompletas = contagens[contagens.ne(MEDICOES_ESPERADAS)]
            if not incompletas.empty:
                print(
                    f"Aviso: {arquivo.name} tem entradas com quantidade diferente "
                    f"de {MEDICOES_ESPERADAS} medicoes:\n{incompletas.to_string()}",
                    file=sys.stderr,
                )

            pasta_cenario = pasta_saida / algoritmo / cenario.removesuffix("_case")
            pasta_cenario.mkdir(parents=True, exist_ok=True)
            tabela_csv = tabela.copy()
            tabela_csv.columns = pd.MultiIndex.from_tuples(CABECALHOS)
            tabela_csv.to_csv(
                pasta_cenario / "tabela.csv",
                index=False,
                float_format="%.10g",
            )
            salvar_imagem(tabela, pasta_cenario / "tabela.png", nome_algoritmo, nome_cenario)
            print(f"\n{nome_algoritmo} — {nome_cenario} (tempos em segundos)")
            print(tabela.to_string(
                index=False, float_format=lambda valor: f"{valor:.8g}",
            ))
            tabelas.append(tabela.assign(Algoritmo=nome_algoritmo, Cenario=nome_cenario))

    if not tabelas:
        raise ValueError(f"Nenhuma medicao encontrada em {pasta_dados}.")

    geral = pd.concat(tabelas, ignore_index=True)
    print(f"\nTabelas salvas em: {pasta_saida}")
    return geral


if __name__ == "__main__":
    gerar_tabelas()
