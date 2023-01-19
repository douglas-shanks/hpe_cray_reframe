import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildRunATPTest(rfm.RegressionTest):
    descr = ('Build and run a test code with ATP enabled')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu']
    modules = ['cpe/22.04','atp/3.14.10']
    env_vars={'ATP_ENABLED': {'1'}, 'OMP_NUM_THREADS': {'1'} }
    sourcesdir = 'src/atp'
    executable = './hello.exe'
    build_system = 'Make'
    num_tasks=2
    num_tasks_per_node=2
    num_cpus_per_task=1
    tags = {'production', 'craype'}
    
    @sanity_function
    def assert_atp(self):
        return sn.all([
            sn.assert_found(r'ATP analysis of Slurm job', self.stderr),            
            sn.assert_found(r'Producing core dumps for rank', self.stderr),
            sn.assert_found(r'View application merged backtrace tree with: stat-view', self.stderr),
            sn.assert_found(r'atpMergedBT_line.dot', self.stderr)])

