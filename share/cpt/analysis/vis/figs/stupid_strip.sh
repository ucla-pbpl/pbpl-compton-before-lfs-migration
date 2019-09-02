#!/bin/sh
awk '/0 0 2400/{for(x=NR-14;x<=NR+5;x++)d[x];}{a[NR]=$0}END{for(i=1;i<=NR;i++)if(!(i in d))print a[i]}' $1
