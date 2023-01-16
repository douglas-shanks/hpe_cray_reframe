# Based on https://github.com/EPCCed/epcc-reframe/blob/master/tests/libs/blas/blas.py
# Author A. Turner EPCC 2022

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class BlasTest(rfm.RegressionTest):
    def __init__(self):
        self.valid_systems = ['archer2']
        self.valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc']

        
        self.prebuild_cmds = []
        self.build_system = 'Make'
        self.build_system.makefile = f'Makefile.libsci'

        self.executable = f'./dgemv_libsci.x'
        self.executable_opts = ['3200','150','10000']

        self.sanity_patterns = sn.assert_found(r'Normal',
                                               self.stdout)

        self.perf_patterns = {
                'normal': sn.extractsingle(r'Normal\s+=\s+(?P<normal>\S+)',
                                     self.stdout, 'normal', float),
                'transpose': sn.extractsingle(r'Transpose\s+=\s+(?P<transpose>\S+)',
                                     self.stdout, 'transpose', float)
        }
        # Lower FLOP/s as default cpu_freq dropped to 2.0GHz 
        # so roughly 30% drop in performance for CPU bound
        self.reference = {
                'archer2:compute': {'normal': (16.75, -0.15, 0.15, 'FLOP/s'),
                                    'transpose': (16.75, -0.15, 0.15, 'FLOP/s')},
                'archer2:login': {'normal': (16.75, -0.15, 0.15, 'FLOP/s'),
                                  'transpose': (16.75, -0.15, 0.15, 'FLOP/s')}
        }
        self.tags = {'performance','functionality','short'}
