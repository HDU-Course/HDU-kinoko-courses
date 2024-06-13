#include "fcntl.h"
#include "semaphore.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "sys/ipc.h"
#include "sys/sem.h"
#include "sys/types.h"
#include "sys/wait.h"
#include "unistd.h"
#define BUF_MAX_SIZE 8192

// 如果x为假，则报错
void CHECK(int x){
    if(!x){
        printf("error appear\n"); // Added newline character for better output formatting
        exit(-1);
    }   
}
int main(int argc, char **argv) {
    int pipefd[2], pid, i = 0;
    int flag = 0;
    ssize_t n; // Added ssize_t n to store the return value of read/write
    char buf[BUF_MAX_SIZE];//管道缓冲池
    char str[BUF_MAX_SIZE];

    sem_t *write_mutex;//sem_t本质上是一个长整形 对于管道进行写操作的互斥信号量
    sem_t *read_mutex1;//进程二三都发完消息的信号量
    sem_t *read_mutex2;
    write_mutex = sem_open("pipe_test_wm", O_CREAT | O_RDWR, 0666, 0);
    read_mutex1 = sem_open("pipe_test_rm_1", O_CREAT | O_RDWR, 0666, 0);
    read_mutex2 = sem_open("pipe_test_rm_2", O_CREAT | O_RDWR, 0666, 0);

    memset(buf, 0, BUF_MAX_SIZE);
    memset(str, 0, BUF_MAX_SIZE);
    
    CHECK(pipe(pipefd) == 0);// 创建管道并检查操作是否成功

    CHECK((pid = fork()) >= 0);// 创建第一个子进程并检查操作是否成功

    // 第一个子进程，利用非阻塞写测试管道大小
    if (pid == 0) {
        int count = 0;
        close(pipefd[0]);//关闭读端
        int flags = fcntl(pipefd[1], F_GETFL);//获取写端状态

        // 管道默认是阻塞写，通过`fcntl`设置成非阻塞写，在管道满无法继续写入时返回-EAGAIN，作为循环终止条件
        fcntl(pipefd[1], F_SETFL, flags | O_NONBLOCK);
    
        // 写入管道
        while (!flag) {
            n = write(pipefd[1], buf, BUF_MAX_SIZE);//一次装入8192B数据 ，因为非阻塞写，所以写满了就会跳出循环，算出管道大小
            if (n == -1) {
                flag = 1;
            } else {
                count++;
                printf("children 1 write %ldB\n", n); // Changed %d to %ld for ssize_t type
            }
        }
        printf("space = %dKB\n", (count * BUF_MAX_SIZE) / 1024);
        exit(0);
    }

    // 创建第二个子进程并检查操作是否成功
    CHECK((pid = fork()) >= 0);
    if (pid == 0) {//当前子进程
        sem_wait(write_mutex);//检查是否有人在写，有则等待
        close(pipefd[0]);//关闭读端
        n = write(pipefd[1], "This is the second children.\n", 29);//写入数据
        printf("children 2 write %ldB\n", n); // Changed %d to %ld for ssize_t type
        sem_post(write_mutex);//释放写权限
        sem_post(read_mutex1);//告诉父进程我信息发完了
        exit(0);//退出该进程
    }

    // 创建第三个子进程并检查操作是否成功
    CHECK((pid = fork()) >= 0);
    if (pid == 0) {
        sem_wait(write_mutex);
        close(pipefd[0]);
        n = write(pipefd[1], "This is the third children.\n", 28);
        printf("children 3 write %ldB\n", n); // Changed %d to %ld for ssize_t type
        sem_post(write_mutex);
        sem_post(read_mutex2);
        exit(0);
    }

    // 等待第一个子进程运行完成，父进程继续运行
    wait(NULL); // Changed 0 to NULL for wait
    close(pipefd[1]);//关闭写端口，父进程读取子进程一的数据清空管道
    int flags = fcntl(pipefd[0], F_GETFL);// 取得文件状态标志

    // 设置非阻塞性读，作为循环结束标志
    fcntl(pipefd[0], F_SETFL, flags | O_NONBLOCK);
    while (!flag) {
        n = read(pipefd[0], str, BUF_MAX_SIZE);
        if (n == -1) {
            flag = 1;
        } else {
            printf("%ldB read\n", n); // Changed %d to %ld for ssize_t type
        }
    }
    sem_post(write_mutex);//释放写权限

    // 等待子进程二、三写入完毕
    sem_wait(read_mutex1);
    sem_wait(read_mutex2);
    n = read(pipefd[0], str, BUF_MAX_SIZE);
    printf("%ldB read\n", n); // Changed %d to %ld for ssize_t type
    for (i = 0; i < n; i++) {
        printf("%c", str[i]);
    }

    sem_close(write_mutex);
    sem_close(read_mutex1);
    sem_close(read_mutex2);
    sem_unlink("pipe_test_wm");
    sem_unlink("pipe_test_rm_1");
    sem_unlink("pipe_test_rm_2");
    return 0;
}