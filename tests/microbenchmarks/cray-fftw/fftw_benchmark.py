# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class FFTWTest(rfm.RegressionTest):
    exec_mode = parameter(['nompi', 'mpi'])
    sourcepath = 'fftw_benchmark.c'
    build_system = 'SingleSource'
    valid_systems = ['archer2:compute']
    # Cray FFTW library is not officially supported for the PGI
    valid_prog_environs = ['PrgEnv-cray', 'PrgEnv-gnu', 'PrgEnv-aocc']
    modules = ['cray-fftw']
    num_tasks_per_node = 12
    maintainers = ['AJ']
    tags = {'benchmark', 'craype'}

    @performance_function('s')
    def fftw_exec_time(self):
        return sn.extractsingle(
            r'execution time:\s+(?P<exec_time>\S+)', self.stdout,
            'exec_time', float
        )

    @sanity_function
    def assert_finished(self):
        return sn.assert_eq(
            sn.count(sn.findall(r'execution time', self.stdout)), 1
        )

    @run_before('compile')
    def set_cflags(self):
        self.build_system.cflags = ['-O2 -fopenmp']

    @run_before('run')
    def configure_exec_mode(self):
        if self.exec_mode == 'nompi':
            self.num_tasks = 12
            self.executable_opts = ['72 12 1000 0']
            self.reference = {
                    'archer2:compute': {
                    'fftw_exec_time': (0.69, None, 0.05, 's'),
                }
            }
        else:
            self.num_tasks = 72
            self.executable_opts = ['144 72 200 1']
            self.reference = {
                    'archer2:compute': {
                    'fftw_exec_time': (0.87, None, 0.50, 's'),
                }
            }
