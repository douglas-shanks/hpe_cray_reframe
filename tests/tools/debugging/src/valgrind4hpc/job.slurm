#! /bin/bash

#SBATCH -p standard
#SBATCH -q standard
#SBATCH -J deadlock
#SBATCH -t 2
#SBATCH -N 1

export OMP_NUM_THREADS=1
module load valgrind4hpc
valgrind4hpc -n 2 --launcher-args="-u" --valgrind-args="--track-origins=yes --leak-check=full" ./test.exe

