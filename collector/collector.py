import csv
import time
import subprocess
import re
import sys


PID=sys.argv[1]


OUT="output/result.csv"



def get_dirty():

    cmd=[
        "python3",
        "soft_dirty.py",
        PID
    ]


    out=subprocess.check_output(
        cmd
    ).decode()


    pages=[]


    for line in out.splitlines():

        if line.startswith("0x"):

            pages.append(
                int(line,16)
            )


    return set(pages)



def parse_damon(line):

    """
    后续根据你的trace格式调整
    """

    m=re.search(
        r'(\w+)-(\w+).*?'
        ,
        line
    )


    return None



with open(
    OUT,
    "w",
    newline=""
) as f:


    writer=csv.writer(f)


    writer.writerow(
        [
            "time",
            "page",
            "access",
            "write"
        ]
    )


    while True:


        dirty=get_dirty()


        now=time.time()


        for page in dirty:


            writer.writerow(
                [
                    now,
                    hex(page),
                    -1,
                    1
                ]
            )


        f.flush()


        time.sleep(1)
