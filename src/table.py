"""Gera tabelas estatisticas dos benchmarks de Insertion Sort e Merge Sort.

Execute da raiz do projeto: .venv/bin/python src/table.py
Dependencias: .venv/bin/python -m pip install -r requirements.txt
"""

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
    limite_inferior = tabela["Media"] - margem
    limite_superior = tabela["Media"] + margem
    tabela["Intervalo de confiança 95% (s)"] = [
        f"[{inferior:.10g}; {superior:.10g}]"
        if pd.notna(inferior) and pd.notna(superior) else "—"
        for inferior, superior in zip(limite_inferior, limite_superior)
    ]
    tabela = tabela.rename(columns={
        "n": "Entrada",
        "Media": "Média (s)",
        "Desvio": "Desvio padrão (s)",
        "Minimo": "Mínimo (s)",
        "Maximo": "Máximo (s)",
    })
    return tabela[[
        "Entrada", "Média (s)", "Desvio padrão (s)",
        "Intervalo de confiança 95% (s)", "Mínimo (s)", "Máximo (s)",
    ]]


def salvar_imagem(tabela, arquivo, nome_algoritmo, nome_cenario):
    """Renderiza as estatisticas em uma imagem PNG legivel."""
    titulos = [
        "Entrada", "Média (s)", "Desvio padrão (s)",
        "Intervalo de confiança 95% (s)", "Mínimo (s)", "Máximo (s)",
    ]
    linhas = []
    for _, linha in tabela.iterrows():
        linhas.append([
            f"{int(linha['Entrada']):,}".replace(",", "."),
            *(
                linha[coluna] if isinstance(linha[coluna], str)
                else "—" if pd.isna(linha[coluna]) else f"{linha[coluna]:.8g}"
                for coluna in tabela.columns[1:]
            ),
        ])

    altura = max(4.8, 1.65 + 0.45 * (len(linhas) + 1))
    figura, eixo = plt.subplots(figsize=(16, altura))
    eixo.axis("off")
    figura.text(
        0.5, 0.94, f"{nome_algoritmo} — {nome_cenario}",
        ha="center", va="center", fontsize=19, fontweight="bold", color="#18334f",
    )
    imagem = eixo.table(
        cellText=linhas,
        colLabels=titulos,
        cellLoc="center",
        colLoc="center",
        colWidths=[0.10, 0.14, 0.16, 0.30, 0.15, 0.15],
        bbox=[0.02, 0.07, 0.96, 0.79],
    )
    imagem.auto_set_font_size(False)
    imagem.set_fontsize(11.5)
    for (indice_linha, _), celula in imagem.get_celld().items():
        celula.set_edgecolor("#d3dce5")
        celula.set_linewidth(0.7)
        if indice_linha == 0:
            celula.set_facecolor("#183b59")
            celula.get_text().set_color("white")
            celula.get_text().set_fontweight("bold")
        else:
            celula.set_facecolor("#ffffff" if indice_linha % 2 else "#f4f7fa")
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
            tabela.to_csv(
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
