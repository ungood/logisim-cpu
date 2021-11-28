from distutils.core import setup

setup(
    name='sappy',
    version='1.0',
    description='Compilers for the SAP series of CPUs',
    url='https://github.com/ungood/logisim-cpu',
    install_requires=[
        'pyparsing[diagrams]',
        'logzero'
    ],
    entry_points = {
        'console_scripts': [
            'sappy=sappy:main'
        ],
    }
)