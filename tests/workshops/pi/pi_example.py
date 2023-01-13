# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import re
import reframe as rfm
import reframe.utility.sanity as sn


class PiBaseTest(rfm.RegressionTest):
    linking = parameter(['dynamic'])
    lang = parameter(['c','f90'])
    prgenv_flags = {}
    descr = 'Brute force calculation of PI by area approximation.'
    sourcepath = 'pi'
    build_system = 'SingleSource'
    prebuild_cmds = ['_rfm_build_time="$(date +%s%N)"']
    postbuild_cmds = [
        '_rfm_build_time="$(($(date +%s%N)-_rfm_build_time))"',
        'echo "Compilations time (ns): $_rfm_build_time"'
    ]
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-aocc', 'PrgEnv-cray', 'PrgEnv-gnu']
    reference = {
        '*': {
            'compilation_time': (60, None, 0.1, 's')
        }
    }
    exclusive_access = True
    tags = {'production', 'craype'}

    @run_after('init')
    def adapt_valid_systems(self):
        if self.linking == 'dynamic':
            self.valid_systems += ['archer2:compute']

    @run_before('compile')
    def prepare_build(self):
        self.env_vars['CRAYPE_LINK_TYPE'] = self.linking
        envname = re.sub(r'(PrgEnv-\w+).*', lambda m: m.group(1),
                         self.current_environ.name)
        try:
            prgenv_flags = self.prgenv_flags[envname]
        except KeyError:
            prgenv_flags = []

        self.build_system.cflags = prgenv_flags
        self.build_system.cxxflags = prgenv_flags
        self.build_system.fflags = prgenv_flags

# FIXME!
#    @sanity_function
#    def assert_diff(self):
#        diff_reference = 0.00000018
#        diff_comp = sn.extractsingle(r'diff = (?P<diff_ex>\S+) %',self.stdout, 'diff_ex', float)
#        energy_diff = sn.abs(diff_comp - diff_reference)
#        return sn.all([
#            sn.assert_lt(energy_diff, 1e-5)
#        ])


    @run_before('sanity')
    def set_sanity(self):
        result = sn.extractsingle(r'diff = \s+(?P<result>\S+)!)',
                self.stdout, 'result', float)
        self.sanity_patterns = sn.assert_reference(result, 0.00000018, None, 1e-5)


    @performance_function('s')
    def compilation_time(self):
        return sn.extractsingle(r'Compilations time \(ns\): (\d+)',
                                self.build_stdout, 1, float) * 1.0e-9

@rfm.simple_test
class PiTestMPIOpenMP(PiBaseTest):
    sourcesdir = 'src'
    num_tasks = 6
    num_tasks_per_node = 3
    num_cpus_per_task = 4

    @run_after('init')
    def set_prgenv_compilation_flags_map(self):
        self.prgenv_flags = {
            'PrgEnv-aocc': ['-fopenmp'],
            'PrgEnv-cray': ['-homp' if self.lang == 'f90' else '-fopenmp'],
            'PrgEnv-gnu': ['-fopenmp'],
        }

    @run_after('init')
    def update_description(self):
        self.descr += ' MPI + OpenMP ' + self.linking.capitalize()

    @run_before('compile')
    def update_sourcepath(self):
        self.sourcepath += '_mpi_openmp.' + self.lang

    @run_before('run')
    def set_omp_env_variable(self):
        # On SLURM there is no need to set OMP_NUM_THREADS if one defines
        # num_cpus_per_task, but adding for completeness and portability
        self.env_vars['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
