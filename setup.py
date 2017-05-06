from setuptools import setup, find_packages

setup(
    name='frcballtracker',
    version='0.1',
    packages=find_packages(),
    url='http://ratchetrockers1706.org',
    license='GPL-3.0',
    author='Connor Monahan',
    author_email='cmonahan@wustl.edu',
    description='Sample of ball tracking routines from various FRC games',
    entry_points={
        'console_scripts': [
            'frcballtracker=frcballtracker.command_line:main'
        ],
    },
)
