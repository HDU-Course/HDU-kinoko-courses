#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <semaphore.h>

sem_t *sem_empty;
sem_t *sem_full;
sem_t *sem_mutex;

int shmid;
void *shmp;

void my_init(){
    sem_empty = sem_open("empty", O_CREAT, 0666, 1);
    sem_full = sem_open("full", O_CREAT, 0666, 0);
    sem_mutex = sem_open("mutex", O_CREAT, 0666, 1);

    shmid = shmget(0x0127, 1024, 0666|IPC_CREAT); 
    shmp = shmat(shmid, NULL, 0);//shmid shmaddr shmflag
}