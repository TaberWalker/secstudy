/*
compile: gcc -fno-stack-protector main.c -ldl
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>

void print_addr() {
    void* handle = dlopen("libc.so.6", RTLD_LAZY);
    printf("%p\n",dlsym(handle,"read"));
    fflush(stdout);
}

void vulnerable_function() {
    char buf[128];
    read(STDIN_FILENO, buf, 256);
}

int main(int argc, char** argv) {
    print_addr();
    write(STDOUT_FILENO, "Hello, World\n", 13);
    vulnerable_function();
}
