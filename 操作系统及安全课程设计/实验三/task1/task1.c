#include <unistd.h> //exit excel 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_CMD_LEN 20 //输入命令最大长度
#define CMD_COLLECTION_LEN 4 //命令数组长度

#define INVALID_COMMAND -1 //未识别命令
#define EXIT 0 //正常退出
#define CMD_1 1
#define CMD_2 2
#define CMD_3 3

#define TRUE 1

char *cmdStr [CMD_COLLECTION_LEN] = {"exit","cmd1","cmd2","cmd3"};
//命令数组

int getCmdIndex(char *cmd)
{//判断输入命令是否合法
    int i;
    for(i=0;i<CMD_COLLECTION_LEN;i++)
    {
        if(strcmp(cmd,cmdStr[i])==0)
        {
            return i;
        }
    }
    return -1;
}

void myFork(int cmdIndex)
{
    pid_t pid;//pid_t 实际上是int型
    if((pid = fork())<0)//fork 子进程是父进程的副本 
    {//fork返回-1说明创建失败，打印fork error
        printf("fork error");
        exit(0);//退出程序
    }
    else if(pid == 0)//fork返回0说明当前运行的是子进程，所以可以进行替换
    {
        int execl_status = -1;//接受execl函数的返回值
        printf("child is running");
        switch(cmdIndex)
        {
            case CMD_1:
                execl_status = execl("./cmd1","cmd1",NULL);
                                //执行程序路径，参数名，最后一个参数须用空指针NULL作结束
                break;
            case CMD_2:
                execl_status = execl("./cmd2","cmd2",NULL);
                break;
            case CMD_3:
                execl_status = execl("./cmd3","cmd3",NULL);
                break;
            default:
                printf("Invalid Command\n");
                break;
        }
        if(execl_status<0)//程序替换失败，即运行失败
        {
            printf("fork error");
            exit(0);
        }
        printf("fork success\n");
        exit(0);
    }
    else
    {
        return;
    }
}
void runCMD(int cmdIndex)
{
    switch(cmdIndex)
    {
        case INVALID_COMMAND://未识别命令
            printf("COMMAND NOT FOUND \n");
            break;
        case EXIT://退出命令
            exit(0);
            break;
        default:
            myFork(cmdIndex);
            break;
    }
}
int main()
{
    pid_t pid;//进程号 
    char cmdStr[MAX_CMD_LEN];
    int cmdIndex;
    while(TRUE)
    {
        printf("\n---Input your command > ");
        scanf("%s",cmdStr);
        cmdIndex = getCmdIndex(cmdStr);//判断合法性命令
        runCMD(cmdIndex);//给出对应反应
        wait(NULL); //父进程一旦调用了wait就立即阻塞自己，由wait自动分析是否当前进程的某个子进程已经退出
        //参数是NULL说明我们不在意子进程是如何结束的 存在一套宏专门用来记录进程结束状态（是否正常退出等）
                printf("waiting for next command");
    }
}