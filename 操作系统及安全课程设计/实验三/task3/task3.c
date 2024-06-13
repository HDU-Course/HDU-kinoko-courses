#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/ipc.h>
#include <sys/msg.h>

#define send_type       1 // 2种 消息类型
#define recv_type       2

#define send_1_to_recv  1                       // 4种 消息走向
#define send_2_to_recv  2
#define recv_to_send_1  3
#define recv_to_send_2  4

void *send_thread_1(void *arg);
void *send_thread_2(void *arg);
void *recv_thread(void *arg);


sem_t send_psx, recv_psx, final_recv_1, final_recv_2;//定义4个信号量类型
pthread_t send_pid_1, send_pid_2, recv_pid;     //声明线程ID

int send_1_over = 0;// sender1线程 是否已经结束
int send_2_over = 0;// sender2线程 是否已经结束

struct msgbuf
{
    long mtype;
    char mtext[256];
    int mdir;// message direction表示消息的走向
};

int msgid;

void *send_thread_1(void *arg)
{
    char info[256];// 消息发送区
    struct msgbuf s_msg;// 消息缓存区
    s_msg.mtype = send_type;// 1
    s_msg.mdir = send_1_to_recv;//消息走向 从发送到接受区
    while (1) {//用户输入
        sem_wait(&send_psx);//申请发送权限
        printf("<Sender1> send: ");
        scanf("%s", info);
        //当用户输入exit时，发送信息停止
        if ((strcmp(info, "exit") == 0)) {
            strcpy(s_msg.mtext, "end1");
            msgsnd(msgid, &s_msg, sizeof(struct msgbuf), 0);
                        /*
                                将消息写入到消息队列
                                <sys/types.h><sys/ipc.h><sys/msg.h>
                                int msgsnd(int msqid[消息队列标识符], const void *msgp[发送给队列的消息], size_t msgsz[要发送消息的大小], int msgflg[消息无法写入时的选择])
                                msgflg:
                                        0：当消息队列满时，msgsnd将会阻塞，直到消息能写进消息队列
                                        IPC_NOWAIT：当消息队列已满的时候，msgsnd函数不等待立即返回
                                        IPC_NOERROR：若发送的消息大于size字节，则把该消息截断，截断部分将被丢弃，且不通知发送进程。
                        */
            sem_post(&recv_psx);//给recv一个信号，有信息在信息队列里面了
            break;
        }
        //正常输入时
                strcpy(s_msg.mtext, info);
        msgsnd(msgid, &s_msg, sizeof(struct msgbuf), 0);//追加一条消息到消息队列中
        sem_post(&recv_psx);
    }

    sem_wait(&final_recv_1);//检查接收线程有没有发送over1消息给线程1   final_recv_1 处理 send_thread_1 最后一次接受消息的问题
    msgrcv(msgid, &s_msg, sizeof(struct msgbuf), recv_type, 0);//从消息队列读取消息   recv_type 2  0 阻塞式接收消息，没有该类型的消息msgrcv函数一直阻塞等待
        /*
                从标识符为msqid的消息队列读取消息并存于s_msg中，读取后把此消息从消息队列中删除
                #include <sys/types.h>
                #include <sys/ipc.h>
                #include <sys/msg.h>
                ssize_t msgrcv(int msqid[消息队列标识符], void *msgp[存放消息的结构体], size_t msgsz[要接收消息的大小], long msgtyp[接受什么样的消息],int msgflg[没有该类型的消息msgrcv函数应该做什么])
                成功：实际读取到的消息数据长度
                出错：-1，错误原因存于error中
                错误代码
                E2BIG：消息数据长度大于msgsz而msgflag没有设置IPC_NOERROR
                EIDRM：标识符为msqid的消息队列已被删除
                EACCESS：无权限读取该消息队列
                EFAULT：参数msgp指向无效的内存地址
                ENOMSG：参数msgflg设为IPC_NOWAIT，而消息队列中无消息可读
                EINTR：等待读取队列内的消息情况下被信号中断
        */
    printf("<Sender1> receive: %s\n", s_msg.mtext);
    
    sem_post(&send_psx);//释放发送权限

    if (send_1_over && send_2_over){//  2个 sender线程 都发送过 'end' 且收到过 'over' 后，将移除消息队列
        msgctl(msgid, IPC_RMID, 0);     // 移除消息队列
                /*
                        <sys/types.h><sys/ipc.h><sys/msg.h>
                        int msgctl ( int msgqid, int cmd, struct msqid_ds *buf[消息队列管理结构体] );
                        IPC_STAT 读取消息队列的数据结构msqid_ds，并将其存储在b u f指定的地址中
                        IPC_SET  设置消息队列的数据结构msqid_ds中的ipc_perm元素的值。这个值取自buf参数
                        IPC_RMID 从系统内核中移走消息队列
                        因为是移除操作，所以buf置零了
                */
    }
    pthread_exit(NULL); // 类比进程的终止 exit()
}

void *send_thread_2(void *arg)
{
    char info[256];// 消息发送区
    struct msgbuf s_msg;// 消息缓存区
    s_msg.mtype = send_type;
    s_msg.mdir = send_2_to_recv;
    while (1) {
        sem_wait(&send_psx);
        
        printf("<Sender2> send: ");
        scanf("%s", info);
        
        if ((strcmp(info, "exit") == 0)) {
            strcpy(s_msg.mtext, "end2");
            msgsnd(msgid, &s_msg, sizeof(struct msgbuf), 0);
            sem_post(&recv_psx);
            break;
        }
        strcpy(s_msg.mtext, info);
        
        msgsnd(msgid, &s_msg, sizeof(struct msgbuf), 0);// 追加一条消息到消息队列中
        sem_post(&recv_psx);
        
    }
    sem_wait(&final_recv_2);// final_recv_2 处理 send_thread_2 最后一次接受消息的问题
    
    msgrcv(msgid, &s_msg, sizeof(struct msgbuf), recv_type, 0);//从消息队列中读一条消息
    printf("<Sender2> receive: %s\n", s_msg.mtext);
    
    sem_post(&send_psx);
    
    if (send_1_over && send_2_over){// 2个 sender 线程 都发送过 'end' 且收到过 'over' 后，将移除消息队列
        msgctl(msgid, IPC_RMID, 0);// 移除消息队列
    }
    pthread_exit(NULL); // 类比进程的终止 exit()
}

void *recv_thread(void *arg)
{
    struct msgbuf r_msg;// 消息缓存区
    while (1) {
        sem_wait(&recv_psx);//首先检查消息队列里有没有消息
        msgrcv(msgid, &r_msg, sizeof(struct msgbuf), send_type, 0);//从消息队列中读取一条消息存到消息缓存区
        if (r_msg.mdir == send_1_to_recv){// 根据消息走向判断来源
            if (strcmp(r_msg.mtext, "end1") == 0) {//是来自发送方的最后一条消息，recv 将“over1”消息写入消息队列
                strcpy(r_msg.mtext, "over1");
                r_msg.mtype = recv_type;
                r_msg.mdir = recv_to_send_1;
                msgsnd(msgid, &r_msg, sizeof(struct msgbuf), 0);
                printf("<Receive_thread> receive 'end1' from <Sender1>, returning 'over1'...\n");
                
                sem_post(&final_recv_1);//告诉线程一收到最后一条消息了
                send_1_over = 1;//线程一结束标志
            }
            else {
                printf("<Receive_thread> receive %s from <Sender1>\n", r_msg.mtext);//打印接收到的消息
                sem_post(&send_psx);//告诉线程我收到消息了
            }
        }
        else if (r_msg.mdir == send_2_to_recv) {// 根据消息走向判断来源
            if (strcmp(r_msg.mtext, "end2") == 0) {
                strcpy(r_msg.mtext, "over2");
                r_msg.mtype = recv_type;
                r_msg.mdir = recv_to_send_2;
                msgsnd(msgid, &r_msg, sizeof(struct msgbuf), 0);
                printf("<Receive_thread> receive 'end2' from <Sender2>, returning 'over1'...");
                
                sem_post(&final_recv_2);
                send_2_over = 1;
                
            }
            else {
                printf("<Receive_thread> receive %s from <Sender>\n", r_msg.mtext);
                sem_post(&send_psx);
            }
        }
        
        
        if (send_1_over && send_2_over){// 2个 sender线程 都发送过 'end' 且收到过 'over' 后，将跳出循环，结束当前线程
            break;
        }
    }
    pthread_exit(NULL);//退出程序
}

int main(void)
{
    sem_init(&send_psx, 0, 1);// pshared = 0，信号量在同一进程的多线程中同步 且线程之间发送信息互斥
    sem_init(&recv_psx, 0, 0);//告诉recv信息对列有几条数据
    sem_init(&final_recv_1, 0, 0);//来自接收线程对线程一的最后一条消息的应答
    sem_init(&final_recv_2, 0, 0);//来自接收线程对线程二的最后一条消息的应答
        /*
                extern int sem_init __P ((sem_t *__sem, int __pshared, unsigned int __value));　　
                sem为指向信号量结构的一个指针
                pshared不为０时此信号量在进程间共享，否则只能为当前进程的所有线程共享
                value给出了信号量的初始值
        */
    
    msgid = msgget(IPC_PRIVATE, 0666|IPC_CREAT);// 创建消息队列
        /*
                int sys_msgget (key_t key, int msgflg)
                {
                        int id;
                        struct msqid_ds *msq;// 设置了私有的标记则直接创建一个新的消息队列

                        if (key == IPC_PRIVATE) 
                                return newque(key, msgflg);
                        // 找不到
                        if ((id = findkey (key)) == -1) { //key not used
                        // 有传IPC_CREAT标记则创建一个新的队列，否则返回找不到
                        if (!(msgflg & IPC_CREAT))
                                return -ENOENT;
                        return newque(key, msgflg);
                }
                // 找到了，但是设置了下面两个标记位说明该消息队列需要由当前进程创建才会返回成功
                if (msgflg & IPC_CREAT && msgflg & IPC_EXCL)
                        return -EEXIST;
                msq = msgque[id];
                // 无效
                if (msq == IPC_UNUSED || msq == IPC_NOID)
                        return -EIDRM;
                // 检查权限
                if (ipcperms(&msq->msg_perm, msgflg))
                        return -EACCES;
                return (unsigned int) msq->msg_perm.seq * MSGMNI + id;
        }
                函数声明： int msgget ( key_t key, int msgflg)
                参数： 
                key：函数ftok的返回值或IPC_PRIVATE(新建一个队列)。 
                msgflag： 
                        IPC_CREAT:创建新的消息队列。 
                        IPC_EXCL:与IPC_CREAT一同使用，表示如果要创建的消息队列已经存在，则返回错误。 
                        IPC_NOWAIT:读写消息队列要求无法满足时，不阻塞。
                返回值： 调用成功返回队列标识符,否则返回-1.
        */
    if (msgid < 0) {
        printf("[*] Error: msgget() return error\n");
        exit(1);
    }
    pthread_create(&send_pid_1, NULL, send_thread_1, NULL);// 创建线程
    pthread_create(&send_pid_2, NULL, send_thread_2, NULL);
    pthread_create(&recv_pid, NULL, recv_thread, NULL);
        /*
                int pthread_create(pthread_t *tidp[指向线程标识符的指针],const pthread_attr_t *attr[设置线程属性],void *(*start_rtn)(void*)[线程运行函数的起始地址],void *arg[运行函数的参数]);

        */
    
    pthread_join(send_pid_1, NULL);     // 阻塞调用 send / receive 线程，否则会出现main函数启动后马上退出
    pthread_join(send_pid_2, NULL);
    pthread_join(recv_pid, NULL);
        /*
                头文件 ： #include <pthread.h>
                函数定义： int pthread_join(pthread_t thread, void **retval);
                描述 ：pthread_join()函数，以阻塞的方式等待thread指定的线程结束。当函数返回时，被等待线程的资源被收回。如果线程已经结束，那么该函数会立即返回。并且thread指定的线程必须是joinable的。
                参数 ：thread: 线程标识符，即线程ID，标识唯一线程。retval: 用户定义的指针，用来存储被等待线程的返回值。
                返回值 ： 0代表成功。 失败，返回的则是错误号。
        */
    
    return 0;
}