#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

void writeFile(unsigned char *content, int content_lenth,
               const char *file_name) {
  printf("write to file \n");
  FILE *f = fopen(file_name, "w+");
  fwrite(content, content_lenth, 1, f);
  fclose(f);
}

int getFileSize(const char *path) {
  int filesize = -1;
  struct stat statbuff;
  if (stat(path, &statbuff) < 0) {
    return filesize;
  } else {
    filesize = statbuff.st_size;
  }
  return filesize;
}

int main(int argc, char *argv[]) {
  int i = 0, j = 388, count = 10;
  unsigned char ucNum = 253, uc1 = 3, uc2 = 13;
  unsigned short usNum = 0;

  memcpy((unsigned char *)&i, &ucNum, 1);
  memcpy((unsigned char *)&i + 1, &ucNum, 1);
  writeFile((unsigned char *)&i, 4, "254.txt");
  writeFile((unsigned char *)&j, 4, "256.txt");

  /* memcpy(&usNum, &uc2, 1); */
  /* memcpy(((unsigned char *)&usNum) + 1, &uc1, 1); */
  /* printf("usNum is %d\n", usNum); */
  /* writeFile((unsigned char *)&usNum, 2, "combined.txt"); */

  usNum = 256;
  writeFile((unsigned char *)&usNum, 2, "combined.txt");

  memcpy(&usNum, &uc1, 1);
  memcpy(((unsigned char *)&usNum) + 1, &uc2, 1);
  printf("usNum is %d\n", usNum);

  return 0;
}
