#
# Affinity check program MPI/OpenMPI
# 
# Makefile for Cray PrgEnv (with Clang CCE C)

CRAY=cray
PGI=pgi
INTEL=intel
GNU=gnu
AOCC=aocc
CLANG=clang
COMPILER:=$($(PE_ENV))

OMP_PGI=-mp
OMP_GNU=-fopenmp
OMP_CRAY=$(OMP_GNU)
OMP_AOCC=$(OMP_GNU)
OMP_INTEL=-openmp
# set this for SLES11 systems
OPTS=-DNEW_VERSION -DNEW_VERSION_PGIFIX -DHAVE_GETCPU

LD_FLAGS_AOCC=-lm

CFLAGS=${OMP_$(PE_ENV)} $(OPTS)
LDFLAGS=${LD_FLAGS_$(PE_ENV)} 

all: acheck #-${COMPILER}

acheck: acheck.c
	cc $(CFLAGS) -o $@ acheck.c

acheck: acheck.c #was acheck-${COMPILER}: acheck.c 
	cc $(CFLAGS) $(LDFLAGS) -o $@ acheck.c

clean:
	$(RM) *.o acheck acheck-cray acheck-aocc acheck-intel acheck-gnu acheck-pgi acheck-clang
