# Specify search path for subroutines that perform 1D ppmlr hydrodynamics
#
# System-dependent parameters 
#
# F90           FORTRAN 90 Compiler
# LDR           Program to load the objects into an executable, typically the same as F90
# LDFLAGS       Flags to pass to the compiler during linking
# LIBS          A list of libraries to link with the executable, normally only netCDF
#
#  currently set for Intel compiler on linux cluster (www.rocksclusters.org)
#                    netcdf data format http://www.unidata.ucar.edu/software/netcdf
#
#LC_ENV=$(shell echo $(PE_ENV) | tr A-Z a-z )

FFLAGS_INTEL = -O2
FFLAGS_CRAY = -O2 -emf
FFLAGS_GNU = -O2
FFLAGS_AOCC= -O2 -march=znver2 -cpp

F90 = ftn
FFLAGS = ${FFLAGS_$(PE_ENV)} -I${NETCDF_DIR}/include
LDR=  ftn
LDRFLAGS=  
LIBS=  -L${NETCDF_DIR}/lib -lnetcdff
#
# List of objects to build multidimensional VH-1 hydro code:

EXE=vh1-mpi #-${LC_ENV}

VHOBJS = vh1mods.o zonemod.o vhone.o dtcon.o dump.o images.o init.o prin.o \
         sweepx1.o sweepx2.o sweepy.o sweepz.o \
         ppmlr.o forces.o flatten.o evolve.o remap.o \
         states.o boundary.o volume.o riemann.o parabola.o

# Lines from here on down should not need to be changed.  They are the
# actual rules which make uses to build the executable
#
.SUFFIXES: .f90 .o

.f90.o:
	$(F90) $(FFLAGS) -c $<

${EXE}:	$(VHOBJS)
	$(LDR) $(LDRFLAGS) -o ${EXE} $(VHOBJS) $(LIBS) #; mkdir -p ../bin; mv ${EXE} ../bin
#
#
clean:
	rm -f *.o *.l *.mod

# Dependencies for the object files
vhone.o:    vhone.f90    global.mod zone.mod sweepsize.mod 
sweepx1.o:  sweepx1.f90  global.mod zone.mod sweepsize.mod sweeps.mod
sweepx2.o:  sweepx2.f90  global.mod zone.mod sweepsize.mod sweeps.mod
sweepy.o:   sweepy.f90   global.mod zone.mod sweepsize.mod sweeps.mod
sweepz.o:   sweepz.f90   global.mod zone.mod sweepsize.mod sweeps.mod
prin.o:     prin.f90     global.mod zone.mod 
dtcon.o:    dtcon.f90    global.mod zone.mod
dump.o:     dump.f90     global.mod zone.mod
images.o:   images.f90   global.mod zone.mod
init.o:     init.f90     global.mod zone.mod

boundary.o: boundary.f90 global.mod sweepsize.mod sweeps.mod
evolve.o:   evolve.f90   global.mod sweepsize.mod sweeps.mod
flatten.o:  flatten.f90  global.mod sweepsize.mod sweeps.mod
forces.o:   forces.f90   global.mod sweepsize.mod sweeps.mod
parabola.o: parabola.f90 global.mod sweepsize.mod
ppmlr.o:    ppmlr.f90    global.mod sweepsize.mod sweeps.mod
remap.o:    remap.f90    global.mod sweepsize.mod sweeps.mod
riemann.o:  riemann.f90  global.mod sweepsize.mod
states.o:   states.f90   global.mod sweepsize.mod sweeps.mod
volume.o:   volume.f90   global.mod sweepsize.mod sweeps.mod





