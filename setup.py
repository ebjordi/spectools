from setuptools import find_namespace_packages
from setuptools import setup
from glob import glob
from os.path import splitext
from os.path import basename

setup(name='spectools',
      version='1.0',
      description='package to handle and plot HERMES, SONG and FIES spectra',
      url='https://github.com/ebjordi/spectools.git',
      author='Jordi Eguren Brown',
      author_email='jordi.eguren.brown@gmail.com',
      packages=find_namespace_packages("src"),
      package_dir={"": "src"},
      py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
      include_package_data=True,
      zip_safe=False,
)
