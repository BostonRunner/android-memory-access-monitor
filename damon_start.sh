#!/bin/bash

PID=$1

if [ -z "$PID" ]; then
    echo "usage: ./damon_start.sh PID"
    exit 1
fi


DAMON=/sys/kernel/mm/damon/admin


echo "configure DAMON"

# create one kdamond
echo 1 > $DAMON/kdamonds/nr_kdamonds


# create context
echo 1 > \
$DAMON/kdamonds/0/contexts/nr_contexts


CTX=$DAMON/kdamonds/0/contexts/0


# virtual address monitor
echo vaddr > $CTX/operations


# one target
echo 1 > $CTX/targets/nr_targets


TARGET=$CTX/targets/0


# monitor PID
echo $PID > $TARGET/pid_target



# sampling interval
echo 5000 > \
$CTX/monitoring_attrs/intervals/sample_us


# aggregation interval
echo 100000 > \
$CTX/monitoring_attrs/intervals/aggr_us


# update interval
echo 1000000 > \
$CTX/monitoring_attrs/intervals/update_us


# region range
echo 10 > \
$CTX/monitoring_attrs/nr_regions/min

echo 100 > \
$CTX/monitoring_attrs/nr_regions/max



# start

echo on > \
$DAMON/kdamonds/0/state


echo "DAMON started for PID=$PID"
