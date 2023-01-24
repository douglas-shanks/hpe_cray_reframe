import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildRunMiniWeatherTest(rfm.RegressionTest):
    # {{{ pe
    descr = ('Build and run the miniWeather mini-app')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu','PrgEnv-aocc'] is currently broken
    modules = ['cray-parallel-netcdf']
    # {{{ compile
    sourcesdir = 'https://github.com/mrnorman/miniWeather.git'
    prebuild_cmds = ['cd fortran']
    #builddir='new_build'
    executable = './fortran/openmp'
    build_system = 'CMake'
    # {{{ prun
    num_tasks=8
    num_tasks_per_node=8
    num_cpus_per_task=16
    tags = {'production','mini-apps','craype'}
    
    @run_before('compile')
    def setflags(self):
        self.build_system.config_opts=['-DCMAKE_Fortran_COMPILER=ftn -DLDFLAGS="-L${CRAY_PARALLEL_NETCDF_DIR}/lib -lpnetcdf" -DNX=400 -DNZ=200 -DSIM_TIME=100 -DOUT_FREQ=1000 -DFFLAGS="-I${CRAY_PARALLEL_NETCDF_DIR}/include"' ]
        if self.current_environ.name.startswith('PrgEnv-cray'):
            self.build_system.config_opts += ['-DOPENMP_FLAGS="-homp"' ]
        elif self.current_environ.name.startswith('PrgEnv-gnu'):
            self.build_system.config_opts += ['-ffree-line-length-none" -DOPENMP_FLAGS="-fopenmp"' ]
        elif self.current_environ.name.startswith('PrgEnv-aocc'):
            self.build_system.config_opts += ['-march=znver2"-DOPENMP_FLAGS="-fopenmp"'  ]

    @run_before('run')
    def set_omp_env_variable(self):
        # On SLURM there is no need to set OMP_NUM_THREADS if one defines
        # num_cpus_per_task,i biut adding for completeness and portability
        self.env_vars['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
        self.env_vars['OMP_PLACES'] = 'cores'
        if self.current_environ.name.startswith('PrgEnv-gnu'):
            self.env_vars['OMP_PROC_BIND'] = 'close'

    @sanity_function
    def assert_diff(self): #d_mass:  1
        regex = (r'd_mass:\s+(?P<result>\S+)')
        result = sn.extractsingle(regex,self.stdout, 'result', float)
        return sn.assert_le(result, 1e-13)



#    @sanity_function
#    def assert_tea(self):
#        return sn.assert_found(r'PASSED', self.stdout)

