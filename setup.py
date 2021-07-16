from setuptools import setup

pennylane_devices_list=[
    'synqs.sqs = pennylane_ls:SingleQuditDevice',
    'synqs.mqs = pennylane_ls:MultiQuditDevice'
]

setup(
    name='pennylane-ls',
    version='0.1.0',
    description='A Pennylane plugin for cold atom quantum simulators',
    url='https://www.github.com/synqs/pennylane-ls',
    author='Fred Jendrzejewski',
    author_email='fnj@kip.uni-heidelberg.de',
    license='BSD-2',
    packages=['pennylane_ls'],
    zip_safe=False,
    install_requires=[
        "pennylane >= 0.16",
        "numpy",
    ],
    entry_points={'pennylane.plugins':pennylane_devices_list} # for registering the pennylane device(s)
)
