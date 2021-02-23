import os
import sys


def compile():
    python_dir = os.path.dirname(sys.executable) + "\\python.exe"
    pckg_dir = os.path.abspath(os.curdir)

    os.system(' & '.join([
        'cd ' + pckg_dir,
        python_dir + ' setup.py sdist bdist_wheel'
    ]))

    r = input("Build successful, upload to testpypi ?")

    if r in ["Y", "y", "1", "ok"]:
        os.system(python_dir + ' -m twine upload --repository testpypi dist/*')


compile()
