from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

from graphics import ler_tabela


ROOT = Path(__file__).resolve().parent.parent
TABLES_DIRECTORY = ROOT / "data" / "tables"
GRAPHICS_DIRECTORY = ROOT / "data" / "graphics"
ALGORITHMS = {
    "insertion": ("Insertion Sort", "#e07828"),
    "merge": ("Merge Sort", "#2378ae"),
}
CASES = {
    "worst": "Pior caso",
    "medium": "Caso médio",
    "best": "Melhor caso",
}


def theoretical_growth(inputs, algorithm, case):
    if algorithm == "merge":
        return inputs * np.log2(inputs), r"n\log_2(n)"
    if case == "best":
        return inputs, "n"
    return inputs ** 2, "n^2"


def polynomial_equation(coefficients):
    terms = []
    for power, coefficient in reversed(list(enumerate(coefficients))):
        if coefficient == 0:
            continue
        mantissa, exponent = f"{abs(coefficient):.4e}".split("e")
        term = fr"{mantissa}\times10^{{{int(exponent)}}}"
        if power == 1:
            term += r"\,n"
        elif power > 1:
            term += fr"\,n^{{{power}}}"
        if not terms:
            terms.append(f"-{term}" if coefficient < 0 else term)
        else:
            sign = "-" if coefficient < 0 else "+"
            terms.append(f"{sign} {term}")
    return r"\widehat{T}(n) = " + (" ".join(terms) or "0")


def generate_chart(algorithm, case, tables_directory, graphics_directory):
    table_file = tables_directory / algorithm / case / "tabela.csv"
    table = ler_tabela(table_file).sort_index()
    inputs = table.index.to_numpy(dtype=float)
    measured_times = table["Média (s)"].to_numpy(dtype=float)

    if (
        inputs.size == 0
        or not np.isfinite(inputs).all()
        or not np.isfinite(measured_times).all()
        or (inputs <= 1).any()
        or (measured_times <= 0).any()
    ):
        raise ValueError(f"Dados inválidos para o modelo teórico em {table_file}.")

    degree = 1 if algorithm == "insertion" and case == "best" else 2
    if inputs.size <= degree:
        raise ValueError(f"Dados insuficientes para a regressão em {table_file}.")
    regression = Polynomial.fit(inputs, measured_times, degree)
    equation = polynomial_equation(regression.convert().coef)

    growth, _ = theoretical_growth(inputs, algorithm, case)
    growth_scale = growth.max()
    scaled_growth = growth / growth_scale
    coefficient = (
        np.dot(scaled_growth, measured_times)
        / np.dot(scaled_growth, scaled_growth)
        / growth_scale
    )
    curve_inputs = np.linspace(inputs.min(), inputs.max(), 400)
    curve_growth, formula = theoretical_growth(curve_inputs, algorithm, case)
    regression_times = regression(curve_inputs)
    algorithm_name, color = ALGORITHMS[algorithm]

    figure, axis = plt.subplots(figsize=(14, 8))
    axis.plot(
        inputs,
        measured_times,
        color=color,
        marker="o",
        linestyle="none",
        markersize=6,
        label="Dados medidos: tempo médio (s)",
        zorder=6,
    )
    axis.plot(
        curve_inputs,
        coefficient * curve_growth,
        color="#172638",
        linestyle="--",
        linewidth=2,
        label=fr"Modelo teórico: $T(n) = c\,{formula}$",
        zorder=5,
    )
    axis.plot(
        curve_inputs,
        regression_times,
        color="#287a43",
        linestyle="-",
        linewidth=2,
        label=fr"Regressão polinomial: ${equation}$",
        zorder=4,
    )
    axis.set_xscale("linear")
    axis.set_yscale("linear")
    axis.set_xlim(left=0)
    axis.set_ylim(bottom=min(0, regression_times.min()))
    axis.ticklabel_format(axis="x", style="plain")
    axis.set_xlabel("Tamanho da entrada (n) — escala linear", fontsize=12)
    axis.set_ylabel("Tempo de execução T(n) (s) — escala linear", fontsize=12)
    axis.set_title(
        f"{algorithm_name} — {CASES[case]}\n"
        "Dados medidos, regressão polinomial e modelo teórico",
        fontsize=18,
        pad=18,
    )
    axis.legend()
    axis.grid(which="major", color="#d8e0e8", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()

    output_directory = graphics_directory / f"{algorithm}_theoretical"
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / f"graph_{algorithm}_theoretical_{case}.png"
    figure.savefig(output_file, dpi=180, facecolor="white")
    plt.close(figure)
    print(f"{algorithm_name} — {CASES[case]}: {output_file}")
    return output_file


def generate_graphics(
    tables_directory=TABLES_DIRECTORY,
    graphics_directory=GRAPHICS_DIRECTORY,
):
    tables_directory = Path(tables_directory)
    graphics_directory = Path(graphics_directory)
    return [
        generate_chart(algorithm, case, tables_directory, graphics_directory)
        for algorithm in ALGORITHMS
        for case in CASES
    ]


if __name__ == "__main__":
    generate_graphics()
