# Insertion Sort and Merge Sort Analysis

This project compares the execution times of Insertion Sort and Merge Sort in three scenarios: best case, average case, and worst case. The C program measures each combination of algorithm and input size 50 times. The Python scripts calculate the mean, standard deviation, 95% confidence interval, minimum, and maximum, then generate tables and comparison charts.

## How to run

Start from the project root. You need GCC and Python 3. To generate new measurements, go to src, compile and run the C program:

```bash
cd src
gcc -o main main.c
./main
```

This step is optional if you already have raw CSV files in `data/insertion` and `data/merge`. It can take several hours and overwrites those files.

Prepare the Python environment once, still from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Ubuntu/Debian, if creating the environment fails because `ensurepip` is missing, install `python3-venv` with `sudo apt install python3-venv`.

Enter `src` and run the table script before the chart script:

```bash
cd src
python table.py
python graphics.py
```

## Project structure

```text
.
├── src/
│   ├── main.c                 # Benchmarks and raw CSV generation
│   ├── table.py               # Statistics, CSV tables, and table images
│   └── graphics.py            # Comparative charts
├── data/                      # Generated locally; ignored by Git
│   ├── insertion/             # Raw Insertion Sort measurements
│   ├── merge/                 # Raw Merge Sort measurements
│   ├── tables/
│   │   └── {insertion,merge}/{best,medium,worst}/
│   │       ├── tabela.csv
│   │       └── tabela.png
│   └── graphics/
│       └── {insertion,merge}/{best,medium,worst}/grafico.png
├── requirements.txt           # Python dependencies
└── README.md
```
