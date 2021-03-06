import sys
from paste.script.command import run

from pkglib.config import org


def main():
    """
    Simply calls 'paster create <opts>', defaulting to the pkglib_project template
    """
    org.setup_global_org_config()

    if not [i for i in sys.argv if i.startswith('-t')]:
        sys.argv = sys.argv[:1] + ['-t', 'pkglib_project'] + sys.argv[1:]
    sys.argv.insert(1, 'create')
    run()

if __name__ == '__main__':
    main()
