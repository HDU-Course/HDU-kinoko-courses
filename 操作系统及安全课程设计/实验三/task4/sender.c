#include "my_shm.h"

int main(){
    my_init();
    int flag=0;

    while(1){
        sem_wait(sem_empty);
        sem_wait(sem_mutex);

        if(flag){
            char recv[100];
            strcpy(recv, (char *)shmp);
            printf("respond: %s\n", recv);
            break;
        }

        printf("send: ");
        char send[100];
        scanf("%s", send);
        if(strcmp(send,"exit")==0)
            flag=1;
        memset((char *)shmp, '\0', 1024);
        strcpy((char *)shmp, send);

        sem_post(sem_mutex);
        sem_post(sem_full);
    } 
    sem_unlink("empty");
    sem_unlink("full");
    sem_unlink("mutex");
    shmdt(shmp);
    shmctl(shmid, IPC_RMID, NULL);//shmid cmd buf
    printf("quit sender!\n");  
    exit(0);
}