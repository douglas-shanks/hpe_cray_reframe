// Code from Cray Programming Models Examples
//
// C/MPI/OpenMP

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include <omp.h>

int main(int argc, char **argv){
  const long long nmax=140000;
  const double pi=3.14159265358979323846264338327950288;
  double diff,mypi,x,y;
  long long count,mycount;
  int i,j,istart,iend,rank,size;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD,&rank);
  MPI_Comm_size(MPI_COMM_WORLD,&size);

  istart = rank * nmax/size;
  iend = (rank+1) * nmax/size - 1;
  if (rank == size-1) iend = nmax-1 ; // for non divisors

  if (rank == 0) printf("PI approximation by MPI/OpenMP program using %d processes and %d threads\n",size,omp_get_max_threads());
 
  mycount = 0;

#pragma omp parallel for default(none) shared(istart,iend,nmax) private(j,x,y) reduction(+:mycount)
  for(i=istart;i<=iend;i++){
    x = (i+0.5)/nmax;
    for(j=0;j<nmax;j++){
      y = (j+0.5)/nmax;
      if ( x*x + y*y < 1.0 ) mycount++;
    }      
  }

  MPI_Reduce(&mycount,&count,1,MPI_LONG_LONG_INT,
             MPI_SUM,0,MPI_COMM_WORLD);

  MPI_Finalize();

  mypi=4*(double)count/nmax/nmax;

  if (!rank)
    printf("   PI = %20.18f\n myPI = %20.18f\n diff = %10.8f%%\n",
           pi,mypi,fabs(mypi-pi)/pi*100);

  return EXIT_SUCCESS;

}


  
