#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    
    // Definir uma nova seed a função de pseudo-randômicos
    srand(time(NULL));

    FILE *evaluated_time_file;
    evaluated_time_file = fopen("evaluated_time.csv", "w");
    fprintf(evaluated_time_file, "size;evaluated_time\n");

    struct timespec start;
    struct timespec end;
    

    // Quantidade de números do vetor A
    //int n = 600000;

    //int qtd[24] = { 1, 10, 25, 50, 75, 100, 125, 150, 250, 500, 750, 1000, 2500, 5000, 7500, 10000, 25000, 50000, 75000, 100000, 250000, 500000, 750000, 1000000 };

    int qtd[16] = { 1, 10, 25, 50, 75, 100, 125, 150, 250, 500, 750, 1000, 2500, 5000, 7500, 10000 };

    for (int i = 0; i < 16; i++) {

        int n = qtd[i];

        // Criado vetor de n números inteiros
        int *A = malloc(sizeof(int) * n);

        // Preencher o vetor com números aleatórios entre 1 e 1000000
        for (int i = 0; i < n; i++) {
            A[i] = (rand() % 1000000) + 1;
        }

        /*  // Visualização do vetor pré ordenação
            printf("Vetor antes da ordenação\n");
            for (int i = 0; i < n; i++) {
                printf("%d ", A[i]);
            }
            printf("\n\n");
        */


        clock_gettime(CLOCK_MONOTONIC, &start);

        // Bubble Sort
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < n; j++) {
                if(A[j] > A[i]) {
                    int temp = A[i];
                    A[i] = A[j];
                    A[j] = temp;
                }
            }
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        double evaluated_time;
        evaluated_time = ((double)end.tv_sec + 1e-9 * end.tv_nsec) - ((double)start.tv_sec + 1e-9 * start.tv_nsec);

        printf("%d - %.8f\n", n, evaluated_time);
        fprintf(evaluated_time_file, "%d;%.8f\n", n, evaluated_time);
        
        /*  // Visualização do vetor pós ordenação
            printf("Vetor depois da ordenação\n");
            for (int i = 0; i < n; i++) {
                printf("%d ", A[i]);
            }
            printf("\n");
        */

        free(A);

    }

    fclose(evaluated_time_file);

    return 0;
}