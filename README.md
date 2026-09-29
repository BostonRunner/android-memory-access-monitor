# android-memory-access-monitor
基于 Android Cuttlefish 和 Linux Kernel
内存接口的应用内存访问行为采集工具。

本项目用于采集 Android 应用运行过程中的：

-   内存区域访问频率；
-   页面访问状态；
-   页面写入状态。

当前版本不修改 Android Framework、ART 或应用代码，仅通过 Linux Kernel
提供的接口进行数据采集。

------------------------------------------------------------------------

## 1. 功能介绍

### 1.1 DAMON Access Monitor

使用 Linux Kernel DAMON（Data Access
MONitor）接口监控指定进程虚拟地址空间。

采集内容：

-   虚拟地址范围；
-   内存区域访问次数；
-   区域活跃时间。

示例：

    PID: 1234
    
    Region:
    0x70000000 - 0x70100000
    
    access_count:
    20
    
    age:
    5

------------------------------------------------------------------------

### 1.2 Soft Dirty Write Monitor

使用 Linux Soft Dirty 机制检测页面写入行为。

流程：

    clear soft dirty bit
            |
    Application running
            |
    Page write
            |
    Kernel marks page dirty
            |
    Read pagemap

输出：

    page address
    write happened: yes/no

------------------------------------------------------------------------

## 2. 系统架构

    Android Application
              |
              |
          Linux Kernel
              |
       +------+------+
       |             |
     DAMON     Soft Dirty
       |             |
    Access     Write Status
       |             |
       +------+------+
              |
         Data Collector
              |
           CSV Output

------------------------------------------------------------------------

## 3. 运行环境

Host:

    Ubuntu 22.04 / Ubuntu 24.04

Device:

    Android Cuttlefish
    x86_64
    Linux 6.x Kernel

需要开启：

    CONFIG_DAMON=y
    CONFIG_DAMON_VADDR=y
    CONFIG_DAMON_SYSFS=y
    CONFIG_PROC_PAGE_MONITOR=y

检查：

``` bash
adb shell zcat /proc/config.gz | grep DAMON
```

------------------------------------------------------------------------

## 4. 文件结构

    android_mem_monitor/
    
    ├── README.md
    
    ├── scripts/
    │   ├── damon_start.sh
    │   ├── damon_stop.sh
    │   └── damon_trace.sh
    
    ├── collector/
    │   ├── collector.py
    │   └── soft_dirty.py
    
    ├── workload/
    │   └── mem_test.c
    
    └── output/
        └── result.csv

------------------------------------------------------------------------

## 5. 使用流程

### 5.1 启动测试程序

编译：

``` bash
clang mem_test.c -o mem_test
```

推送：

``` bash
adb push mem_test /data/local/tmp/
```

运行：

``` bash
adb shell /data/local/tmp/mem_test
```

获取 PID：

``` bash
adb shell pidof mem_test
```

------------------------------------------------------------------------

### 5.2 启动 DAMON

``` bash
./scripts/damon_start.sh <PID>
```

------------------------------------------------------------------------

### 5.3 查看 DAMON 输出

``` bash
./scripts/damon_trace.sh
```

输出：

    damon_aggregated
    
    target_id=1234
    start=0x70000000
    end=0x70100000
    nr_accesses=20
    age=5

------------------------------------------------------------------------

### 5.4 Soft Dirty 采集

``` bash
python3 collector/soft_dirty.py <PID>
```

------------------------------------------------------------------------

### 5.5 综合采集

``` bash
python3 collector/collector.py <PID>
```

输出：

    output/result.csv

------------------------------------------------------------------------

## 6. 数据格式

result.csv:

    timestamp,
    pid,
    page_address,
    access_count,
    write_flag

字段：

  字段           说明

-------------- --------------------

  timestamp      采集时间
  pid            进程 ID
  page_address   页面虚拟地址
  access_count   DAMON访问次数
  write_flag     Soft Dirty检测结果

------------------------------------------------------------------------

## 7. 测试程序

`workload/mem_test.c`

用于生成简单内存访问行为。

包含：

### Read Access

``` c
sum += buffer[i];
```

### Write Access

``` c
buffer[i] = value;
```

用于验证采集工具是否能够捕获：

-   高频访问区域；
-   写入区域。

------------------------------------------------------------------------

## 8. 当前限制

### 8.1 访问粒度

DAMON 返回区域访问统计，不是 CPU 指令级 load/store。

### 8.2 写入信息

Soft Dirty 可以判断页面是否发生写入，但不能统计写次数。

### 8.3 访问类型

当前无法直接获得：

    read count
    write count

仅提供：

    access frequency
    write touched status

------------------------------------------------------------------------

## 9. 输出结果

采集结果可用于分析：

-   应用运行期间内存访问变化；
-   不同内存区域访问频率；
-   页面写入活跃情况；
-   内存访问时间序列。

------------------------------------------------------------------------

## Reference

Linux DAMON:

https://docs.kernel.org/mm/damon/

Linux pagemap:

https://docs.kernel.org/admin-guide/mm/pagemap.html

Linux Soft Dirty:

https://docs.kernel.org/admin-guide/mm/soft-dirty.html
