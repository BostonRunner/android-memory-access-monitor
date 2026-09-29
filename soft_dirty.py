#!/usr/bin/env python3

import os
import struct
import time


PAGE_SIZE = 4096


def clear_soft_dirty(pid):

    path=f"/proc/{pid}/clear_refs"

    with open(path,"w") as f:
        f.write("4")



def read_maps(pid):

    regions=[]

    with open(f"/proc/{pid}/maps") as f:

        for line in f:

            addr=line.split()[0]

            start,end=[
                int(x,16)
                for x in addr.split("-")
            ]

            regions.append(
                (start,end)
            )

    return regions



def read_soft_dirty(pid):

    result={}


    maps=read_maps(pid)


    with open(
        f"/proc/{pid}/pagemap",
        "rb"
    ) as f:


        for start,end in maps:


            addr=start


            while addr<end:


                index=(addr//PAGE_SIZE)*8


                f.seek(index)


                data=f.read(8)


                if len(data)!=8:
                    break


                entry=struct.unpack(
                    "Q",
                    data
                )[0]


                # bit55

                dirty=(entry>>55)&1


                if dirty:

                    result[addr]=1


                addr+=PAGE_SIZE


    return result



if __name__=="__main__":

    pid=int(os.sys.argv[1])


    clear_soft_dirty(pid)


    time.sleep(1)


    dirty=read_soft_dirty(pid)


    print(
        "dirty pages:",
        len(dirty)
    )


    for p in list(dirty)[:20]:

        print(hex(p))
