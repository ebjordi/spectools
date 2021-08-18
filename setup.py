from setuptools import setup

setup(name='spectools',
      version='0.1',
      description='HERMES and SONG tools',
      url='https://github.com/jordi5/spectools.git',
      author='Jordi Eguren Brown',
      author_email='jordi.eguren.brown',
      license='MIT',
      packages=['spectools','orbit'],
      zip_safe=False,
      install_requires=[
      "numpy",
      "pandas",
      "astropy",
      "specutils",
      "pyspeckit",
      "scipy")
