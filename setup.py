from setuptools import setup, find_packages

setup(
    name='memoplat',
    version='0.0.1',
    packages=find_packages(exclude='venv'),
    url='https://github.com/kuronbo/memoplat',
    license='MIT',
    author='kuronbo',
    author_email='kurinbo.i2o@gmail.com',
    description='manage plane memory',
    install_requires=['SQLAlchemy'],
)
