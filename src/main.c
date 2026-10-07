// gcc -o main main.c
// ./main

#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <sys/stat.h>

// Declaracao de funcoes

int *fillArraySorted(int *Array, int input);
int *fillArrayRandom(int *Array, int input);
int *fillArrayInverted(int *Array, int input);


void merge(int arr[], int l, int m, int r){
    
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[], int l, int r){
    
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}

void mergeSortBenchmarkBestCase(
    FILE *benchmarkInsertion, 
    int input,
    struct timespec timer_start, 
    struct timespec timer_end,
    int *Array
){
    double total_time;
    fillArraySorted(Array, input);

    for (int i = 0; i < 50; i++){

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        mergeSort(Array, 0, input - 1);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("%d - MERGE SORT: Loop %d de 50 concluido - MELHOR CASO\n",input, i + 1);
    }
}

void mergeSortBenchmarkMediumCase(
    FILE *benchmarkInsertion, 
    int input,
    struct timespec timer_start, 
    struct timespec timer_end,
    int *Array
){
    double total_time;
    srand(time(NULL));

    for (int i = 0; i < 50; i++){
        
        fillArrayRandom(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        mergeSort(Array, 0, input - 1);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("%d - MERGE SORT: Loop %d de 50 concluido - MEDIO CASO\n",input, i + 1);
    }
}

void mergeSortBenchmarkWorstCase(
    FILE *benchmarkInsertion, 
    int input,
    struct timespec timer_start, 
    struct timespec timer_end,
    int *Array
){
    double total_time;
    

    for (int i = 0; i < 50; i++){

        fillArrayInverted(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        mergeSort(Array, 0, input - 1);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("%d - MERGE SORT: Loop %d de 50 concluido - PIOR CASO\n",input, i + 1);
    }
}

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

// Melhor caso (vetor com valores de 1 até 𝑛 em ordem crescente)
void insertionSortBenchmarkBestCase(
        FILE *benchmarkInsertion, 
        int input,
        struct timespec timer_start, 
        struct timespec timer_end,
        int *Array
){
    
    double total_time;

    fillArraySorted(Array, input);

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
    
    
    for (int i = 0; i < 50; i++){

        fillArrayRandom(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        insertionSort(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("%d - INSERTION SORT: Loop %d de 50 concluido - MEDIO CASO\n", input, i + 1);

        // Desordena o vetor novamente
        fillArrayRandom(Array, input);
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

    for (int i = 0; i < 50; i++){

        fillArrayInverted(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        insertionSort(Array, input);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);
        printf("%d - INSERTION SORT: Loop %d de 50 concluido - PIOR CASO\n", input, i + 1);

    }
}

int* fillArraySorted(int *Array, int input){
    int counter = 1;

    for (int j = 0; j < input; j++){
        Array[j] = counter;
        counter++;
    }

    return Array;
}

int* fillArrayRandom(int *Array, int input){
    
    for (int i = 0; i < input; i++) {
        Array[i] = (rand() % 1000000) + 1;
    }

    return Array;
}

int* fillArrayInverted(int *Array, int input){
    for (int j = 0; j < input; j++) {
        Array[j] = input - j;
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
        insertionSortBenchmarkMediumCase(benchmarkInsertionMediumCase, n, timer_start, timer_end, Array);
        insertionSortBenchmarkWorstCase(benchmarkInsertionWorstCase, n, timer_start, timer_end, Array);

        mergeSortBenchmarkBestCase(benchmarkMergeBestCase, n, timer_start, timer_end, Array);
        mergeSortBenchmarkMediumCase(benchmarkMergeMediumCase, n, timer_start, timer_end, Array);
        mergeSortBenchmarkWorstCase(benchmarkMergeWorstCase, n, timer_start, timer_end, Array);

        free(Array);
    }

    fclose(benchmarkInsertionBestCase);
    fclose(benchmarkInsertionMediumCase);
    fclose(benchmarkInsertionWorstCase);

    fclose(benchmarkMergeBestCase);
    fclose(benchmarkMergeMediumCase);
    fclose(benchmarkMergeWorstCase);

    return 0;
}


