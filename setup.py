from distutils.core import setup
from setuptools import find_packages

import stylecheck

requires = ['argparse>=1.2.1',
            'docopt==0.6.1',
	   ]

setup(name='stylecheck',
      version=stylecheck.__version__,
      description='Style checker for multiple languages',
      keywords='style check lint analysis guideline',
      author='Erich Schroeter',
      author_email='erich.schroeter+stylecheck@gmail.com',
      url='http://github.com/erichschroeter/sc',
      scripts=['bin/sc',],
      packages=find_packages('.', exclude=['tests*']),
      package_dir={'stylechecker': 'stylechecker'},
      install_requires=requires,
      )
