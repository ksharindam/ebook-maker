from setuptools import setup
from setuptools.command.bdist_wheel import bdist_wheel
from subprocess import check_call


# allows to run commands before building wheel
class BdistWheel(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        check_call("pyrcc5 -o ./ebook_maker/resources_rc.py ./data/resources.qrc".split())
        check_call("make --directory=lib".split())

setup(
    name='ebook-maker',
    packages=['ebook_maker'],
    #version="2.3",
    entry_points={
      'gui_scripts': ['ebook_maker=ebook_maker.main:main'],
    },
    data_files=[
        ('share/applications', ['data/ebook-maker.desktop']),
        ('share/icons/hicolor/scalable/apps', ['data/ebook-maker.png'])
    ],
    cmdclass = {'bdist_wheel': BdistWheel},
    include_package_data=True,
    zip_safe=False
)
