#!/bin/bash


TRACE=/sys/kernel/tracing


echo 1 > \
$TRACE/events/damon/damon_aggregated/enable


cat \
$TRACE/trace_pipe
