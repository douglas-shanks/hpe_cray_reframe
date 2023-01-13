! Code from Cray Programming Models Examples
!
! Fortran MPI/OpenACC

  program getpi
  use mpi
  use omp_lib
  implicit none
  integer(selected_int_kind(9)),parameter :: i64=selected_int_kind(18)
  double precision, parameter :: pi=3.14159265358979323846264338327950288D0
  integer, parameter :: nmax=140000
  double precision diff,mypi,x,y
  integer i,j,istart,iend,ier,rank,size
  integer(kind=i64) count,mycount

  call MPI_Init(ier)
  call MPI_Comm_rank(MPI_COMM_WORLD,rank,ier)  
  call MPI_Comm_size(MPI_COMM_WORLD,size,ier)  

  istart = rank * nmax/size
  iend = (rank+1) * nmax/size - 1

  if (rank == size-1) iend = nmax - 1 ! for non divisors

  if (rank==0) print '(a,i0,a,i0,a)',&
 &              "PI approximation by MPI program using ",&
 &              size," processes and ",omp_get_max_threads()," threads"


  mycount=0

!$omp parallel do default(private) shared(istart,iend) reduction(+:mycount)
  do i=istart,iend
   x=(i+0.5D0)/nmax
   do j=0,nmax-1
    y=(j+0.5D0)/nmax
    if (x*x+y*y<1d0) mycount=mycount+1
    end do
  end do

! No standard way to send fortran integers with KIND values by MPI...
  call MPI_Reduce(mycount,count,1,MPI_INTEGER8,&
&                    MPI_SUM,0,MPI_COMM_WORLD,ier)

  call MPI_Finalize(ier)

  mypi=4*dble(count)/nmax/nmax

  if (rank==0) then
    print "('   PI = ',f20.18/' myPI = ',f20.18/' diff = ',f10.8,'%')",&
&       pi,mypi,abs(mypi-pi)/pi*100
    end if

 
  end

  
  
