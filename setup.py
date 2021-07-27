from setuptools import setup, find_packages

setup(
    name='jbwsl2',
    version='1.0.0',
    license='GNU GPLv3',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    package_data={'': ['*.png']},
    url='https://github.com/cedriclevarlet/jetbrains.invalid-interpolation',
    author='Cédric Le Varlet',
    author_email='cedric@levarlet.fr',
    description='A curious way to resolve the invalid-interpolation errors which occurs on JetBrain\'s IDEs when attempting to run a docker-compose application in WSL2.',
    entry_points={'console_scripts': ['jbwsl2 = bin.jbwsl2:run']},
    install_requires=[
        'PyQt6>=6.0.0'
    ]
)
