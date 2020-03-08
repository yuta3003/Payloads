#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]){
  char buf[32];

  if(argc < 2){
    printf("Usage: %s <string>\n", argv[0]);
    return 1;
  }

  strcpy(buf, argv[1]);
  printf("%s\n", buf);

  return 0;
}
