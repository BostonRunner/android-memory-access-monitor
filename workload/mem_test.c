#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


#define SIZE (128*1024*1024)


int main()
{

    char *buf;

    buf=
    malloc(SIZE);


    printf(
        "pid=%d\n",
        getpid()
    );


    while(1)
    {


        // read

        long sum=0;


        for(
            int i=0;
            i<SIZE;
            i+=4096
        )
        {
            sum+=buf[i];
        }



        // write

        for(
            int i=0;
            i<SIZE;
            i+=4096
        )
        {
            buf[i]=1;
        }


        sleep(1);

    }


}
