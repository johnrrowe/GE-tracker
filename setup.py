from setuptools import setup, find_packages

setup(name='GE-tracker',
      version='0.1',
      packages=find_packages(),
      install_requires = ["pandas>=0.24.2",
                          "requests>=2.22.0",
                          "matplotlib>=3.0.3",
                          "mysql-connector-python-rf>=2.2.2"])
