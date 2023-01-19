import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class BuildRunValgrind4HPCTest(rfm.RegressionTest):
    def __init__(self):
        # {{{ pe
        self.descr = ('Build and run a test code with valgrind4hpc')
        self.valid_systems = ['archer2:compute']
        self.valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu']
        self.tool='valgrind4hpc'
        self.modules = [self.tool]
    #env_vars = {'LD_LIBRARY_PATH': '${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}'}
        self.tags = {'cpu', 'craype', 'debugging'}
        # {{{ compile
        self.sourcesdir = 'src/valgrind4hpc'
        self.executable = self.tool
        self.target_executable = './test.exe'
        self.build_system = 'Make'
        # {{{ run
        self.time_limit = '10m'
        self.num_tasks=2
        self.num_tasks_per_node=2
        self.num_cpus_per_task=1
        self.env_vars={'OMP_NUM_THREADS': {'1'} }
    
        self.sanity_patterns =  sn.all([
            sn.assert_found(r'HEAP SUMMARY', self.stdout),
            sn.assert_found(r'LEAK SUMMARY', self.stdout),
            sn.assert_found(r'ERROR SUMMARY', self.stdout)])

    # {{{ set_launcher
    @run_before('run')
    def set_launcher(self):
        # The job launcher has to be changed because
        # the tool can be called without srun
        self.job.launcher = getlauncher('local')()
    # }}}

    # {{{ set_opts
    @run_before('run')
    def set_opts(self):
        self.tool_opts = (
            f' -n{self.num_tasks}'
            f' --launcher-args="-u"'
            f' --valgrind-args="--track-origins=yes --leak-check=full"'
            f' --from-ranks=0-0 '
            # f' --from-ranks=0-{self.num_tasks-1} '
            # f' --launcher-args=""'
        )
        self.executable_opts = [
            self.tool_opts, self.target_executable, '--',
        ]        
