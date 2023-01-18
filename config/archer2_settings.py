# https://github.com/EPCCed/epcc-reframe/blob/master/configuration/archer2_settings.py
import os
from pathlib import Path
import json

# Get root dir
root_dir = Path(__file__).parent

archer2_login_topo = json.load(
    open(os.path.join(root_dir, 'topologies', 'archer2_login.json'), 'r')
)
archer2_compute_topo = json.load(
    open(os.path.join(root_dir, 'topologies', 'archer2_compute.json'), 'r')
)


site_configuration = {
    'systems': [
        {
            'name': 'archer2',
            'descr': 'ARCHER2',
            'hostnames': ['uan','ln'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'login',
                    'descr': 'Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['PrgEnv-gnu','PrgEnv-cray','PrgEnv-aocc'],
                    'processor': {
                        **archer2_login_topo,
                        },
                },
                {
                    'name': 'compute',
                    'descr': 'Compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['--hint=nomultithread','--distribution=block:block','--partition=standard', '--qos=short'],
                    'environs': ['PrgEnv-gnu','PrgEnv-cray','PrgEnv-aocc'],
                    'max_jobs': 16,
                    'processor': {
                        **archer2_compute_topo,
                        },
                    #'resources': [
                    #    {
                    #        'name': 'qos',
                    #        'options': ['--qos={qos}']
                    #    }
                    #]
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'PrgEnv-gnu',
            'modules': ['PrgEnv-gnu'],
            'cc': 'cc',
            'cxx': 'CC',
            'ftn': 'ftn',
            'target_systems': ['archer2']
        },
        {
            'name': 'PrgEnv-cray',
            'modules': ['PrgEnv-cray'],
            'cc': 'cc',
            'cxx': 'CC',
            'ftn': 'ftn',
            'target_systems': ['archer2']
        },
        {
            'name': 'PrgEnv-aocc',
            'modules': ['PrgEnv-aocc'],
            'cc': 'cc',
            'cxx': 'CC',
            'ftn': 'ftn',
            'target_systems': ['archer2']
        },
    ],
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                }
            ]
        }
    ],
}
