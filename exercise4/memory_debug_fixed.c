#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int* allocate_memory(int size) {
    int* arr = (int*)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        arr[i] = i;
    }
    return arr;
}

void free_memory(int* arr) {
    // Fix 1: Actually free the memory
    free(arr);
    printf("Memory freed\n");
}

int main() {
    int* my_array = allocate_memory(5);

    printf("Array contents: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", my_array[i]);
    }
    printf("\n");

    // Create another allocation
    int* array_copy = allocate_memory(5);
    memcpy(array_copy, my_array, 5 * sizeof(int));

    free_memory(my_array);
    // Fix 2: Free array_copy as well
    free_memory(array_copy);

    return 0;
}
