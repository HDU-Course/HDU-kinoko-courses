#include "my_shm.h"

int main(){
    my_init();
    int flag=0;
    while(1){
        sem_wait(sem_full);
        sem_wait(sem_mutex);

        char recv[100];
        strcpy(recv, (char *)shmp);
        printf("receive: %s\n",recv);
        
        if(strcmp(recv, "exit") == 0){
            char send[100]="over";
            memset((char *)shmp, '\0', 1024);
            strcpy((char *)shmp, send);
            flag=1;
        }

        sem_post(sem_empty);
        sem_post(sem_mutex);  

        if(flag) break;
    }
    shmdt(shmp);
    printf("quit receiver!\n");
    exit(0);
}