#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <CMakeConfig.h>

void print_usage() {
  printf("Usage: server TCP\n");
}

void exec_prog(char* prog_name, char* prog_argv[]) {
  if (execvp(prog_name, prog_argv) == -1) {
    perror(prog_name);
    exit(1);
  }
}

void parse(int argc, char* argv[]) {
  if (argc < 2) {
    print_usage();
    exit(1);
  }

  if (strcasecmp(argv[1], "TCP") == 0) {
    char prog_name[256];
    strcpy(prog_name, SRC_DIRECTORY);
    strcat(prog_name, "default-tcp/tcp-server");
    printf("prog_name: %s\n", prog_name);

    char** prog_argv = &argv[1];
    prog_argv[0] = prog_name; 

    exec_prog(prog_name, prog_argv);
    return;
  }
}

int main(int argc, char* argv[]) {
  parse(argc, argv);

  return 0;
}
