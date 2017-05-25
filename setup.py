import setuptools
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension


def get_setup():
    return dict(
        name='pymbd',
        version='0.2',
        description='Many-body dispersion method',
        long_description='See README.md for details.',
        author='Jan Hermann',
        author_email='dev@hermann.in',
        url='https://github.com/azag0/mbd',
        packages=['pymbd'],
        ext_modules=[Extension(**get_mbdlib())],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Programming Language :: Fortran',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Physics',
        ],
        license='Mozilla Public License 2.0',
        cmdclass={'build_ext': get_build_ext()},
        install_requires=['numpy'],
        test_suite='pymbd.tests',
    )


def get_build_ext():
    # patch build_ext to include the temporary build directory to include_dirs
    # so that the module files from building mbdlib are seen when building the
    # extension
    from numpy.distutils.command.build_ext import build_ext as _build_ext

    class build_ext(_build_ext):
        def build_extension(self, ext):
            ext.include_dirs.append(self.build_temp)
            _build_ext.build_extension(self, ext)

    return build_ext


def get_mbdlib():
    from numpy.distutils.system_info import get_info
    sources = ['src/mbd_interface.f90', 'src/mbd_helper.f90']
    try:
        import mpi4py
    except ImportError:
        sources.insert(0, 'src/mpi_stubs.f90')
    else:
        # patch find_executables to insert the MPI compiler before FC or
        # --f90exec is checked
        from numpy.distutils.fcompiler import FCompiler
        from functools import wraps
        _find_executables = FCompiler.find_executables
        @wraps(FCompiler.find_executables)  # noqa
        def find_executables(self):
            self.executables['compiler_f90'][0] = mpi4py.get_config()['mpif90']
            return _find_executables(self)
        FCompiler.find_executables = find_executables
    args = dict(
        name='pymbd.lib',
        sources=['src/mbd.f90'],
        libraries=[
            ('mbdlib', dict(
                sources=sources,
                language='f90',
            ))
        ],
    )
    for arg, val in get_info('lapack_opt', 2).items():
        if arg == 'libraries':
            args['libraries'].extend(val)
        else:
            args[arg] = val
    return args


setup(**get_setup())
