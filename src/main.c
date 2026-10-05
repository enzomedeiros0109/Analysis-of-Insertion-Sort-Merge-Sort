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

    struct timespec timer_start;
    struct timespec timer_end;

    int quantity[10] = {
        1000, 2000, 5000, 10000, 20000,
        50000, 100000, 200000, 500000, 1000000
    };

    for (int i = 0; i < 1; i++){

        int n = quantity[i];
        int *ArrayInsertion = malloc(sizeof(int) * n );
        int *ArrayMerge = malloc(sizeof(int) * n );

        // Preenchendo vetor para melhor caso (vetor com valores de 1 até 𝑛 em ordem crescente)
        int counter = 1;

        for (int j = 0; j < n; j++){
            ArrayInsertion[j] = counter;
            counter++;
        }

        clock_gettime(CLOCK_MONOTONIC, &timer_start);

        // Insertion Sort
        insertionSort(ArrayInsertion, n);

        clock_gettime(CLOCK_MONOTONIC, &timer_end);

        double total_time;
        total_time = ((double) timer_end.tv_sec + 1e-9 * timer_end.tv_nsec) - ((double)timer_start.tv_sec + 1e-9 * timer_start.tv_nsec);
        
        fprintf(benchmarkInsertion, "%d,%.8f\n", n, total_time);

        free(ArrayInsertion);
    }

    fclose(benchmarkInsertion);
    fclose(benchmarkMerge);

    return 0;
}

void insertionSortBenchmark(){

}


