#include<stdlib.h>
#include<mpi.h>

int main(int argc, char *argv[])
{
	MPI_Init(&argc,&argv);

	int rank;
	int *a = (int*) malloc(sizeof(int)*5);

	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	if(rank==0)
	{
		for(int i=0;i<10;i++)
			a[i] = i;
	}

	MPI_Finalize();

	return 0;
}

