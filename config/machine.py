# Template for a new machine. Fill in the blanks, see archer2 as an example.
site_configuration = {
    'systems': [
        {
            'name': '',
            'descr': '',
            'hostnames': ['',''],
            'modules_system': '',
            'partitions': [
                {
                    'name': '',
                    'descr': '',
                    'scheduler': '',
                    'launcher': '',
                    'environs': [''],
                },
                {
                    'name': '',
                    'descr': '',
                    'scheduler': '',
                    'launcher': '',
                    'access': [''],
                    'environs': [''],
                    'max_jobs': ,
                    'resources': []
                }
            ]
        }
    ],
    # These are kept as examples, add more if necessary
    'environments': [
        {
            'name': 'PrgEnv-gnu',
            'modules': ['PrgEnv-gnu'],
            'cc': 'cc',
            'cxx': 'CC',
            'ftn': 'ftn',
            'target_systems': ['']
        },
        {
            'name': 'PrgEnv-cray',
            'modules': ['PrgEnv-cray'],
            'cc': 'cc',
            'cxx': 'CC',
            'ftn': 'ftn',
            'target_systems': ['']
        },
        {
            'name': 'PrgEnv-aocc',
            'modules': ['PrgEnv-aocc'],
            'cc': 'cc',
            'cxx': 'CC',
            'ftn': 'ftn',
            'target_systems': ['']
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
