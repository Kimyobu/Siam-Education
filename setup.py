import argparse
import subprocess
import importlib.util
from importlib.metadata import version

def run(cmd: str):
    return subprocess.run(f"{cmd}", shell=True)

def is_installed(name: str, pkg_version: str or None = None, operator: str = '=='):
    out = False
    try:
        package = importlib.util.find_spec(name)
        if package is not None:
            out = True
            if pkg_version is not None:
                ver = version(package.name)
                if operator == '==':
                    out = (ver == pkg_version)
                elif operator == '>=':
                    out = (ver >= pkg_version)
                elif operator == '<=':
                    out = (ver <= pkg_version)
                elif operator == '<':
                    out = (ver < pkg_version)
                elif operator == '>':
                    out = (ver > pkg_version)
                elif operator == '!=':
                    out = (ver != pkg_version)
                elif operator == '~=':
                    out = (pkg_version in package.requires)
    except ModuleNotFoundError:
        pass
    return out

def run_pip(install_syntax: str):
    operators = ['<', '>', '==', '>=', '<=' , '!=']
    found = []

    for op in operators:
        if op in install_syntax:
            found.append(op)

    operator = found[-1] if len(found) > 0 else '=='

    if operator is not None:
        package_info = install_syntax.split(operator)
        name = package_info[0].strip()
        version = package_info[1].strip() if len(package_info) > 1 else None

        if is_installed(name, version, operator) is False and name != '':
            print(f'Install {install_syntax}')
            run(f"pip install --no-cache-dir -q {install_syntax}")
            
def install_req(file):
    op = open(file, 'r')
    r = op.read()
    op.close()
    for x in r.split('\n'):
        run_pip(x)

install_req("requirements.txt")