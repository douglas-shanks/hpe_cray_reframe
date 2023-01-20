
/*The Parallel Hello World Program*/
#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv)
{
	int my_rank,
	    sendbuf,
	    recvbuf,
	    count,
	    tag;

	MPI_Comm comm;
	MPI_Status status;
   
	MPI_Init(&argc,&argv);

	count = 1;
	tag = 1;
	comm = MPI_COMM_WORLD;
	MPI_Comm_rank (comm, &my_rank);
	if (my_rank == 0) 
	{
		MPI_Recv (&recvbuf, count, MPI_INT, 1, tag, comm, &status);
		MPI_Send (&sendbuf, count, MPI_INT, 1, tag, comm);
	} 
	else if (my_rank == 1) 
	{
		MPI_Recv (&recvbuf, count, MPI_INT, 0, tag, comm, &status);
		MPI_Send (&sendbuf, count, MPI_INT, 0, tag, comm);
	}

	MPI_Finalize();
}
