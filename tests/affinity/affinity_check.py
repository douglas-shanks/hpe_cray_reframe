#Based on similar CSCS and EPCC scripts

import re
import reframe as rfm
import reframe.utility.sanity as sn


class AffinityBaseTest(rfm.RegressionTest):
    linking = parameter(['dynamic'])
    lang = parameter(['c'])
    prgenv_flags = {}
    sourcepath = 'affinity.c'
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
    tags = {'functionality', 'short'}

    @run_after('init')
    def set_description(self):
        lang_names = {
            'c': 'C'
        }
        self.descr = f'{lang_names[self.lang]} Hello, World'

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

    @run_after('init')
    def set_prgenv_compilation_flags_map(self):
        self.prgenv_flags = {
            'PrgEnv-aocc': ['-fopenmp'],
            'PrgEnv-cray': ['-homp' if self.lang == 'f90' else '-fopenmp'],
            'PrgEnv-gnu': ['-fopenmp'],
        }

    @run_before('sanity')
    def set_sanity(self):

        def parse_cpus(x):
            return sorted(x)

        re_aff_cores = r'affinity = \s+(?P<cpus>\d+:\d+:(?:[\d+,]*|[\d+-]*)\d+)'
        self.aff_cores = sn.extractall(
            re_aff_cores, self.stdout, 'cpus', parse_cpus)
        ref_key = 'ref_' + self.current_partition.fullname
        self.ref_cores = sn.extractall(
            re_aff_cores, self.cases[ref_key],
            'cpus', parse_cpus)

        # Ranks and threads can be extracted into lists in order to compare
        # them since the affinity programm prints them in ascending order.
        self.sanity_patterns = sn.all([
            sn.assert_eq(sn.sorted(self.aff_cores), sn.sorted(self.ref_cores))
        ])


    @performance_function('s')
    def compilation_time(self):
        return sn.extractsingle(r'Compilations time \(ns\): (\d+)',
                                self.build_stdout, 1, float) * 1.0e-9

@rfm.simple_test
class AffinityTestOpenMP(AffinityBaseTest):
    descr = 'Checking core affinity for OMP threads.'
    sourcesdir = 'src'
    cases = {
                'ref_archer2:compute': 'archer2_numa_omp.txt',
                'num_cpus_per_task_archer2:compute': 16,
                'num_tasks': 8,
                'num_tasks_per_node': 8,
                'num_cpus_per_task': 16,
                'OMP_PLACES': 'cores'}
    num_tasks=cases['num_tasks']
    num_tasks_per_node = cases['num_tasks_per_node']
    num_cpus_per_task = cases['num_cpus_per_task']

    @run_after('init')
    def update_description(self):
        self.descr += ' OpenMP ' + self.linking.capitalize()

    @run_before('run')
    def set_tasts_omp_env_variable(self):
        # On SLURM there is no need to set OMP_NUM_THREADS if one defines
        # num_cpus_per_task, but adding for completeness and portability
        partname = self.current_partition.fullname
        self.num_cpus_per_task = self.cases['num_cpus_per_task_%s' % partname]
        self.num_tasks = 1
        self.env_vars  = {
            'OMP_NUM_THREADS': str(self.num_cpus_per_task),
            'OMP_PLACES': self.cases['OMP_PLACES']
        }

@rfm.simple_test
class AffinityTestMPI_full_nosmt(AffinityBaseTest):
    descr = 'Checking core affinity for MPI processes. Fully populated with no SMT threads'
    valid_systems = ['archer2:compute']
    cases = {
                'ref_archer2:compute': 'archer2_fully_populated_nosmt.txt',
                'runopts_archer2:compute': ['--hint=nomultithread', '--distribution=block:block'],
                'num_tasks': 128,
                'num_tasks_per_node': 128,
                'num_cpus_per_task': 1,
        }
    num_tasks = cases['num_tasks']
    num_tasks_per_node =cases['num_tasks_per_node']
    num_cpus_per_task = cases['num_cpus_per_task']

    @run_before('run')
    def set_launcher(self):
        partname = self.current_partition.fullname
        self.job.launcher.options = self.cases['runopts_%s' % partname]

@rfm.simple_test
class AffinityTestMPI_full_smt(AffinityBaseTest):
    descr = 'Checking core affinity for MPI processes. Fully populated with SMT threads'
    valid_systems = ['archer2:compute']
    cases = {
                'ref_archer2:compute': 'archer2_fully_populated_smt.txt',
                'runopts_archer2:compute': ['--ntasks=256', '--ntasks-per-node=256', '--hint=multithread', '--distribution=block:block'],
                'num_tasks': 128,
                'num_tasks_per_node': 128,
                'num_cpus_per_task': 1 }
    num_tasks = cases['num_tasks']
    num_tasks_per_node =cases['num_tasks_per_node']
    num_cpus_per_task = cases['num_cpus_per_task']

    @run_before('run')
    def set_launcher(self):
        partname = self.current_partition.fullname
        self.job.launcher.options = self.cases['runopts_%s' % partname]

@rfm.simple_test
class AffinityTestMPI_proc_per_numa(AffinityBaseTest):
    descr = 'Checking core affinity for MPI processes. Single process per NUMA'
    valid_systems = ['archer2:compute']
    cases = {
               'ref_archer2:compute': 'archer2_single_process_per_numa.txt',
                'runopts_archer2:compute': ['--hint=nomultithread', '--distribution=block:block'],
                'num_tasks': 8,
                'num_tasks_per_node': 8,
                'num_cpus_per_task': 16 }
    num_tasks = cases['num_tasks']
    num_tasks_per_node =cases['num_tasks_per_node']
    num_cpus_per_task = cases['num_cpus_per_task']

    @run_before('run')
    def set_launcher(self):
        partname = self.current_partition.fullname
        self.job.launcher.options = self.cases['runopts_%s' % partname]


