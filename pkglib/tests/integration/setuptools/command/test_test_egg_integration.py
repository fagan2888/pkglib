from __future__ import print_function
import copy
import os

from pkglib_testing.util import PkgTemplate
from pkglib.pyenv import PythonInstallation

HERE = os.getcwd()


def test_test_egg(pytestconfig):
    """ Creates template, runs setup.py test_egg
    """
    with PkgTemplate(name='acme.foo-1.0.0.dev1') as pkg:
        pkg.run('python %s/bin/easy_install %s' %
                (pkg.virtualenv, pkg.trunk_dir))

        pkg.install_package('pytest-cov')
        print(pkg.run_with_coverage(['%s/setup.py' % pkg.trunk_dir, 'test_egg'],
                                    pytestconfig, cd=HERE))
        py_env = PythonInstallation(pkg.python)
        egg = 'test.acme.foo-1.0.0.dev1-%s.egg' % py_env.py_version()
        egg = os.path.join(pkg.trunk_dir, 'dist', egg)
        assert os.path.isfile(egg)

        # Now install it and run the tests
        pkg.run('python %s/bin/easy_install %s' % (pkg.virtualenv, egg))

        # XXX stripping coverage/pylint off for now, fix this later - it should
        # work
        new_env = copy.copy(pkg.env)
        if 'BUILD_TAG' in new_env:
            del(new_env['BUILD_TAG'])

        pkg.run_with_coverage(['%s/bin/runtests' % (pkg.virtualenv), 'acme.foo'],
                              pytestconfig, cd=HERE, env=new_env)
