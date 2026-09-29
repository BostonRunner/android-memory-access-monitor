#!/bin/bash


DAMON=/sys/kernel/mm/damon/admin


echo off > \
$DAMON/kdamonds/0/state


echo "DAMON stopped"
