// gcc -o main main.c
// ./main

#include <stdlib.h>
#include <time.h>
#include <stdio.h>

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

int insertionSortBenchmark(
        FILE *benchmarkInsertion, 
        int input,
        struct timespec timer_start, 
        struct timespec timer_end,
        int *Array
    ){

    // Melhor caso (vetor com valores de 1 até 𝑛 em ordem crescente)
    int counter = 1;

    for (int j = 0; j < input; j++){
        Array[j] = counter;
        counter++;
    }

    clock_gettime(CLOCK_MONOTONIC, &timer_start);

    // Insertion Sort
    insertionSort(Array, input);

    clock_gettime(CLOCK_MONOTONIC, &timer_end);

    double total_time;
    total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
    
    fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);

    // Caso médio (vetor preenchido com valores gerados aleatoriamente)

    srand(time(NULL));

    for (int i = 0; i < input; i++) {
        Array[i] = (rand() % 1000000) + 1;
    }

    clock_gettime(CLOCK_MONOTONIC, &timer_start);

    insertionSort(Array, input);

    clock_gettime(CLOCK_MONOTONIC, &timer_end);

    total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
    
    fprintf(benchmarkInsertion, "%d,%.8f\n", input, total_time);

}

int main(){
    
    srand(time(NULL));

    // Preparação para os arquivos CSV
    FILE *benchmarkInsertion;
    benchmarkInsertion = fopen("benchmark_insertion.csv", "w");

    FILE *benchmarkMerge;
    benchmarkMerge = fopen("benchmark_merge.csv", "w");

    char* entriesTitle = "Entradas";
    char* timeTitle = "Tempo";

    fprintf(benchmarkInsertion, "%s, %s (s)\n", entriesTitle, timeTitle);
    fprintf(benchmarkMerge, "%s, %s (s)\n", entriesTitle, timeTitle);

    // Variáveis para contagem de tempo
    struct timespec timer_start;
    struct timespec timer_end;

    // Entradas
    int inputs[10] = {
        1000, 2000, 5000, 10000, 20000,
        50000, 100000, 200000, 500000, 1000000
    };

    for (int i = 0; i < 10; i++){

        int n = inputs[i];
        int *Array = malloc(sizeof(int) * n );

        insertionSortBenchmark(benchmarkInsertion, n, timer_start, timer_end, Array);
        free(Array);
    }

    fclose(benchmarkInsertion);
    fclose(benchmarkMerge);

    return 0;
}


