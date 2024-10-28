#include <stdio.h>
#include <stdlib.h>


void swap(int arr[], int a, int b){
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
}
int partitition(int arr[], int p, int r){
    int x = arr[r];
    int i = p -1;
    for(int j = p; j < r; j++){
        if (arr[j] <= x){
            i++;
            swap(arr, i, j);
        }
    }
    swap(arr,i+1, r);
    return i +1;

}
void quicksort(int arr[], int p, int r){
    if(p < r){
        int q = partitition(arr, p,r);
        quicksort(arr,p, q -1);
        quicksort(arr, q+1, r);
    }
}

int main(){
    int arr[5] = {1,2,6,7,5};
    quicksort(arr, 0, 4);
    for(int i = 0; i < 5; i++){
        printf("%d \n", arr[i]);
    }
}