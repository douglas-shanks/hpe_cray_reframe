import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildRunVH1IOTest(rfm.RegressionTest):
    descr = ('Build and run the VH1 mini-app')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']
    modules = ['cray-hdf5','cray-netcdf'] #,'cpe/22.04']
    #env_vars = {'LD_LIBRARY_PATH': '${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}'}
    env_vars={'NO_STOP_MESSAGE': {'1'}, 'OMP_NUM_THREADS': {'1'}, 'STRIPE_SIZE': {'4m'}, 'STRIPE_COUNT': {'1'} }
    sourcesdir = 'src'
    executable = './vh1-mpi'
    build_system = 'Make'
    num_tasks=128
    num_tasks_per_node=128
    num_cpus_per_task=1
    prerun_cmds = ['lfs setstripe -c ${STRIPE_COUNT} -S ${STRIPE_SIZE} output']
    postrun_cmds =['cat output/NCState.hst']
    tags = {'production', 'craype'}

    @sanity_function
    def assert_vh1(self):
        return sn.assert_found(r'successful stop', self.stdout)

