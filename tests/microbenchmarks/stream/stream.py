# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher


@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    def __init__(self):
        self.descr = 'STREAM Benchmark'
        self.exclusive_access = True
        self.valid_systems = ['archer2:compute']
        self.valid_prog_environs = ['PrgEnv-cray', 'PrgEnv-gnu',
                                    'PrgEnv-aocc']

        #self.use_multithreading = False # This will add --hint=nomultithread

        self.prgenv_flags = {
            'PrgEnv-cray': ['-fopenmp', '-O3','-hmodel=large','-DSTREAM_ARRAY_SIZE=2600000000'],
            'PrgEnv-gnu': ['-fopenmp', '-O3', '-mcmodel=large', '-DSTREAM_ARRAY_SIZE=2600000000'],
            'PrgEnv-aocc': ['-fopenmp', '-O3', '-mcmodel=large', '-DSTREAM_ARRAY_SIZE=2600000000'],
        }

        self.sourcepath = 'stream.c'
        self.build_system = 'SingleSource'
        self.tool = './Stream'
        self.executable = self.tool
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.stream_cpus_per_task = {
            'archer2:compute': 16,
        }
        self.env_vars = {
            'OMP_PLACES': '"{0:8}:16:8"',
            'OMP_PROC_BIND': 'spread',
            'OMP_NUM_THREADS' : '16'
        }
        self.sanity_patterns = sn.assert_found(
            r'Solution Validates: avg error less than', self.stdout)
        self.perf_patterns = {
            'triad': sn.extractsingle(r'Triad:\s+(?P<triad>\S+)\s+\S+',
                                      self.stdout, 'triad', float)
        }
        self.stream_bw_reference = {
            'PrgEnv-cray': {
                'archer2:compute': {'triad': (200000, -0.05, None, 'MB/s')},
            },
            'PrgEnv-gnu': {
                'archer2:compute': {'triad': (200000, -0.05, None, 'MB/s')},
            },
            'PrgEnv-aocc': {
                'archer2:compute': {'triad': (200000, -0.05, None, 'MB/s')},
            },
        }
        self.tags = {'production', 'craype'}

    @run_after('setup')
    def prepare_test(self):
        self.num_cpus_per_task = self.stream_cpus_per_task.get(
            self.current_partition.fullname, 1)
        self.env_vars['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
        envname = self.current_environ.name

        self.build_system.cflags = ['-fopenmp -O3 -mcmodel=medium -DSTREAM_ARRAY_SIZE=2600000000']


        #self.build_system.cflags = self.prgenv_flags.get(envname, ['-O3 -fopenmp'])
        #self.variables['OMP_PROC_BIND'] = 'true'

        try:
            self.reference = self.stream_bw_reference[envname]
        except KeyError:
            self.reference = self.stream_bw_reference['PrgEnv-gnu']           

    # {{{ set_launcher
    @run_before('run')
    def set_launcher(self):
        # The job launcher has to be changed because
        # the tool can be called without srun
        self.job.launcher = getlauncher('local')()
    # }}}
