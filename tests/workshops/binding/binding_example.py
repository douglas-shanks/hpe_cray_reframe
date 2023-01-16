# Based on https://github.com/EPCCed/epcc-reframe/blob/master/tests/libs/blas/blas.py
# Author A. Turner EPCC 2022

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class AcheckTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['archer2']
        self.valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']
        self.prebuild_cmds = []
        self.build_system = 'Make'
        self.build_system.makefile = f'Makefile'
        self.executable = f'./acheck'
        self.executable_opts = ['-v']
        self.num_tasks = 8
        self.num_tasks_per_node = 8
        self.num_cpus_per_task= 16

        # Fix me add more than just this check
        self.sanity_patterns = sn.assert_found(r'MPI and OpenMP Affinity Checker v1.23', self.stdout)

        self.tags = {'functionality','short'}
