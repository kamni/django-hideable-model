import os
from setuptools import setup, find_packages


ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-disabled-model',
    version='0.1',
    description='Django plugin to allow model objects in the db that are disabled',
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    author='Jay Leadbetter',
    author_email='codemonkey@jleadbetter.com',
    url='http://bitbucket.org/kamni/django-disabled-model',
    license='Affero GPL v3',
    packages=find_packages(exclude=['tests', 'tests/*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.5'], 
    tests_require=['django-nose>=1.2'],
    # TODO: include classifiers
)