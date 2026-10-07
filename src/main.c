// gcc -o main main.c
// ./main

#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <sys/stat.h>

// Declaracao de funcoes

int *fillArrayRandom(int *Array, int input);
int *fillArrayInverted(int *Array, int input);

void insertionSort(int arr[], int n){
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
                            
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

// Caso médio (vetor preenchido com valores gerados aleatoriamente)
void insertionSortBenchmarkMediumCase(
        FILE *benchmarkInsertion, 
        int input,
        struct timespec timer_start, 
        struct timespec timer_end,
        int *Array
){
    double total_time;

    srand(time(NULL));
    fillArrayRandom(Array, input);
    
    for (int i = 0; i < 50; i++){

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        insertionSort(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("INSERTION SORT: Loop %d de 50 concluido - MEDIO CASO\n", i + 1);

        // Desordena o vetor novamente
        fillArrayRandom(Array, input);
    }
}

// Melhor caso (vetor com valores de 1 até 𝑛 em ordem crescente)
void insertionSortBenchmarkBestCase(
        FILE *benchmarkInsertion, 
        int input,
        struct timespec timer_start, 
        struct timespec timer_end,
        int *Array
    ){
    
    double total_time;
    int counter = 1;

    for (int j = 0; j < input; j++){
        Array[j] = counter;
        counter++;
    }

    // Rodando o teste 50 vezes
    for (int i = 0; i < 50; i++){

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        insertionSort(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("%d - INSERTION SORT: Loop %d de 50 concluido - MELHOR CASO\n",input, i + 1);
    }
}

// Pior caso (vetor com valores de 𝑛 até 1 em ordem decrescente)
void insertionSortBenchmarkWorstCase(
        FILE *benchmarkInsertion, 
        int input,
        struct timespec timer_start, 
        struct timespec timer_end,
        int *Array
    ){
    
    double total_time;

    fillArrayInverted(Array, input);

    for (int i = 0; i < 50; i++){

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        insertionSort(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("INSERTION SORT: Loop %d de 50 concluido - PIOR CASO\n", i + 1);

        fillArrayInverted(Array, input);
    }
}

int* fillArrayRandom(int *Array, int input){
    
    for (int i = 0; i < input; i++) {
        Array[i] = (rand() % 1000000) + 1;
    }

    return Array;
}

int* fillArrayInverted(int *Array, int input){
    int counter = input;

    for (int j = input; j > 0; j--){
        Array[j] = counter;
        counter--;
    }

    return Array;
}

int main(){

    // Criacao de diretorios

    mkdir("../data", 0777);
    mkdir("../data/insertion", 0777);
    mkdir("../data/merge", 0777);

    // ARQUIVOS CSV INSERTION

    FILE *benchmarkInsertionBestCase;
    benchmarkInsertionBestCase = fopen("../data/insertion/benchmark_insertion_best_case.csv", "w");

    FILE *benchmarkInsertionMediumCase;
    benchmarkInsertionMediumCase = fopen("../data/insertion/benchmark_insertion_medium_case.csv", "w");

    FILE *benchmarkInsertionWorstCase;
    benchmarkInsertionWorstCase = fopen("../data/insertion/benchmark_insertion_worst_case.csv", "w");

    // ARQUIVOS CSV MERGE

    FILE *benchmarkMergeBestCase;
    benchmarkMergeBestCase = fopen("../data/merge/benchmark_merge_best_case.csv", "w");

    FILE *benchmarkMergeMediumCase;
    benchmarkMergeMediumCase = fopen("../data/merge/benchmark_merge_medium_case.csv", "w");

    FILE *benchmarkMergeWorstCase;
    benchmarkMergeWorstCase = fopen("../data/merge/benchmark_merge_worst_case.csv", "w");

    // Cabecalho
    char* entriesTitle = "Entradas";
    char* timeTitle = "Tempo";

    // Escrevendo cabecalho dos arquivos INSERTION
    fprintf(benchmarkInsertionBestCase, "%s, %s (s)\n", entriesTitle, timeTitle);
    fprintf(benchmarkInsertionMediumCase, "%s, %s (s)\n", entriesTitle, timeTitle);
    fprintf(benchmarkInsertionWorstCase, "%s, %s (s)\n", entriesTitle, timeTitle);

    // Escrevendo cabecalho dos arquivos INSERTION
    fprintf(benchmarkMergeBestCase, "%s, %s (s)\n", entriesTitle, timeTitle);
    fprintf(benchmarkMergeMediumCase, "%s, %s (s)\n", entriesTitle, timeTitle);
    fprintf(benchmarkMergeWorstCase, "%s, %s (s)\n", entriesTitle, timeTitle);

    // Variáveis para contagem de tempo
    struct timespec timer_start;
    struct timespec timer_end;

    // Definir uma nova seed a função de pseudo-randômicos
    srand(time(NULL));

    // Entradas
    int inputs[10] = {
        1000, 2000, 5000, 10000, 20000,
        50000, 100000, 200000, 500000, 1000000
    };

    for (int i = 0; i < 10; i++){

        int n = inputs[i];
        int *Array = malloc(sizeof(int) * n );

        insertionSortBenchmarkBestCase(benchmarkInsertionBestCase, n, timer_start, timer_end, Array);
        // insertionSortBenchmarkMediumCase(benchmarkMergeMediumCase, n, timer_start, timer_end, Array);
        // insertionSortBenchmark(benchmarkMergeWorstCase, n, timer_start, timer_end, Array);
        free(Array);
    }

    fclose(benchmarkInsertionBestCase);
    fclose(benchmarkMergeBestCase);

    return 0;
}


