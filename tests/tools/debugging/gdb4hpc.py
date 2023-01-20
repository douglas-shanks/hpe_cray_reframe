import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class BuildRunGDB4HPCTest(rfm.RegressionTest):
    def __init__(self):
        # {{{ pe
        self.descr = ('Build and run a test code with gdb4hpc. Here we just test launch.')
        self.valid_systems = ['archer2:login']
        self.valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu']
        self.tool='gdb4hpc'
        self.modules = [self.tool]
        self.tags = {'cpu', 'craype', 'debugging'}
        # {{{ compile
        self.sourcesdir = 'src/gdb4hpc'
        self.executable = self.tool
        #self.target_executable = './deadlock'
        self.build_system = 'Make'
        # {{{ run
        self.time_limit = '10m'
        self.num_tasks=2
        self.num_tasks_per_node=2
        self.num_cpus_per_task=1
        self.gdb_in = './gdb4hpc.in'
        self.executable_opts = [f'-b {self.gdb_in} #']

        self.sanity_patterns =  sn.all([
            sn.assert_found(r'Cray Line Mode Parallel Debugger', self.stdout),
            sn.assert_found(r'show breakpoint           Show information about breakpoints', self.stdout),
            sn.assert_found(r'Shutting down debugger and killing application', self.stdout)])

    # {{{ set_launcher
    @run_before('run')
    def set_launcher(self):
        # The job launcher has to be changed because
        # the tool can be called without srun
        self.job.launcher = getlauncher('local')()
    # }}}
