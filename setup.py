
import os
from setuptools import setup
from distutils.cmd import Command
from ebook_maker import __version__

class Build(Command):
    description = 'build c/c++ extensions'
    user_options = []     # The format is [long option, short option, description]
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system("make --directory=lib")

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ebook-maker',
    packages=['ebook_maker'],
    version=__version__,
    description='Images to PDF document converter',
    long_description= readme(),
    long_description_content_type = 'text/markdown',
    keywords='documents ebook pdf pyqt pyqt5 qt5',
    url='http://github.com/ksharindam/ebook-maker',
    author='Arindam Chaudhuri',
    author_email='ksharindam@gmail.com',
    license='GNU GPLv3',
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications :: Qt',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    ],
    entry_points={
      'console_scripts': ['ebookmaker=ebook_maker.main:main'],
    },
    data_files=[
             ('share/applications', ['files/ebook-maker.desktop']),
             ('share/icons', ['files/ebook-maker.png'])
    ],
    cmdclass = {'compile' : Build},     # using {'build' : Build} gives error
    include_package_data=True,
    zip_safe=False
)
