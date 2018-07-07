
from setuptools import setup
from ebook_maker import __version__


setup(
      name='ebook_maker',
      version=__version__,
      description='Images to PDF document converter',
      long_description='Images to PDF document converter',
      keywords='documents ebook pdf pyqt pyqt5 qt5',
      url='http://github.com/ksharindam/ebook-maker',
      author='Arindam Chaudhuri',
      author_email='ksharindam@gmail.com',
      license='GNU GPLv3',
      packages=['ebook_maker'],
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
      ],
      include_package_data=True,
      zip_safe=False)
