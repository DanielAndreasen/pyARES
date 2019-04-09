from setuptools import setup, find_packages
from Cython.Distutils import build_ext


setup(
	maintainer='Daniel T. Andreasen',
    name='ARES',
	version=0.1,
	long_description=open('README.md').read(),
	license='MIT',
    packages=find_packages(),
    url='https://github.com/DanielAndreasey/pyARES',
    cmdclass={'build_ext': build_ext},
	install_requires=[
		'numpy>=1.15.0',
		'matplotlib>=2.0.2',
		'pandas>=0.23.0'
	]
)
