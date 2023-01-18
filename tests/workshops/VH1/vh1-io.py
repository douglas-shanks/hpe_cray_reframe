import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildRunVH1IOTest(rfm.RegressionTest):
    descr = ('Build and run the VH1 mini-app')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']
    sourcesdir = 'src/src'
    executable = './bin/vh1-mpi'
    build_system = 'Make'
    num_tasks=128
    num_tasks_per_node=128
    num_cpus_per_task=1
    tags = {'production', 'craype'}

    @sanity_function
    def assert_vh1(self):
        return sn.assert_found(r'successful stop', self.stdout)

