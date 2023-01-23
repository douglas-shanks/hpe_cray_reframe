import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildRunTealeafTest(rfm.RegressionTest):
    descr = ('Build and run the Tealeaf mini-app')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']
    modules = ['cpe/22.04']
    #self.sourcesdir = None
    sourcesdir = 'https://github.com/UK-MAC/TeaLeaf_ref.git'
    executable = './tea_leaf'
    build_system = 'Make'
    num_tasks=8
    num_tasks_per_node=8
    num_cpus_per_task=16
    tags = {'production', 'craype'}

    @run_before('compile')
    def setflags(self):
        if self.current_environ.name.startswith('PrgEnv-gnu'):
            self.build_system.options = ['MPI_COMPILER=ftn C_MPI_COMPILER=cc C_OPTIONS="-O3 -fopenmp" OPTIONS="-O3 -fopenmp -fallow-argument-mismatch"']
        elif self.current_environ.name.startswith('PrgEnv-cray'):
            self.build_system.options = ['MPI_COMPILER=ftn C_MPI_COMPILER=cc C_OPTIONS="-O3 -fopenmp" OPTIONS="-O3 -homp -eZ"']
        elif self.current_environ.name.startswith('PrgEnv-aocc'): # AOCC will fail with v2.X due to a compiler bug
            self.build_system.options = ['MPI_COMPILER=ftn C_MPI_COMPILER=cc C_OPTIONS="-O3 -fopenmp -march=znver2" OPTIONS="-O3 -fopenmp -march=znver2 -cpp"']

    @run_before('run')
    def set_omp_env_variable(self):
        # On SLURM there is no need to set OMP_NUM_THREADS if one defines
        # num_cpus_per_task,i biut adding for completeness and portability
        self.env_vars['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
        self.env_vars['OMP_PLACES'] = 'cores'
        if self.current_environ.name.startswith('PrgEnv-gnu'):
            self.env_vars['OMP_PROC_BIND'] = 'close'

    @sanity_function
    def assert_tea(self):
        return sn.assert_found(r'PASSED', self.stdout)

