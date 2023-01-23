import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class BuildRunPerftoolsLiteTest(rfm.RegressionTest):
    # {{{ pe
    descr = ('Build and run a test code with Perftools-lite')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']
    modules = ['perftools-base','perftools-lite']
    #env_vars = {'LD_LIBRARY_PATH': '${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}'}
    tags = {'cpu', 'craype', 'debugging'}
    # {{{ compile
    sourcesdir = 'src'
    executable = './himeno.exe'
    build_system = 'Make'
    # {{{ run
    time_limit = '10m'
    num_tasks=8
    num_cpus_per_task=1
    env_vars={'OMP_NUM_THREADS': {'1'} }
    
    @run_before('compile')
    def setflags(self):
        if self.current_environ.name.startswith('PrgEnv-gnu'):
            self.build_system.options = ['FCFLAGS="-fallow-argument-mismatch"']
        elif self.current_environ.name.startswith('PrgEnv-aocc'): 
            self.build_system.options = ['FCFLAGS="-march=znver2 -cpp"']

    @sanity_function
    def assert_perftoolslite(self):
        return sn.all([sn.assert_found(r'CrayPat-lite Performance Statistics', self.stdout),
            sn.assert_found(r'Avg Process Time:', self.stdout),
            sn.assert_found(r'High Memory:', self.stdout),
            sn.assert_found(r'I/O Write Rate:', self.stdout),
            sn.assert_found(r'End of CrayPat-lite output', self.stdout)])
