import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class BuildRunATPTest(rfm.RegressionTest):
    descr = ('Build and run a test code with ATP enabled')
    valid_systems = ['archer2:compute']
    valid_prog_environs = ['PrgEnv-cray','PrgEnv-gnu']
    modules = ['cpe/22.04','atp/3.14.10']
    #env_vars = {'LD_LIBRARY_PATH': '${CRAY_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}'}
    env_vars={'ATP_ENABLED': {'1'}, 'OMP_NUM_THREADS': {'1'} }
    sourcesdir = 'src/atp'
    executable = './hello.exe'
    build_system = 'Make'
    num_tasks=2
    num_tasks_per_node=2
    num_cpus_per_task=1
#    prerun_cmds = ['lfs setstripe -c ${STRIPE_COUNT} -S ${STRIPE_SIZE} output']
#    postrun_cmds =['cat output/NCState.hst']
    tags = {'production', 'craype'}
    
    @sanity_function
    def assert_atp(self):
        return sn.all([
            sn.assert_found(r'ATP analysis of Slurm job', self.stderr),            
            sn.assert_found(r'Producing core dumps for rank', self.stderr),
            sn.assert_found(r'View application merged backtrace tree with: stat-view', self.stderr),
            sn.assert_found(r'atpMergedBT_line.dot', self.stderr)])

        
#        re_stderr_1 = 'Producing core dumps for rank'
#        re_stderr_2 = 'View application merged backtrace tree with: stat-view'
        #re_stderr_3 = 'atpMergedBT_line.dot'

#        self.sanity_patterns = sn.all([
                # check the job output:
                # check the tool output:
#                sn.assert_found(re_stderr_1, self.stderr),
#                sn.assert_found(re_stderr_2, self.stderr),
                #sn.assert_found(re_stderr_3, self.stderr),
#            ])
