import os
from setuptools import setup, find_packages

import filemanager


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-filemanager',
    version=filemanager.__version__,
    description='Template for reusable django applications.',
    long_description=read('README.md'),
    license='BSD',
    author='byteweaver',
    author_email='contact@byteweaver.org',
    url='https://github.com/byteweaver/django-reusable-app-template',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'django',
    ],
    tests_require=[
        'coverage',
        'django-coverage',
        'factory-boy',
    ],
    test_suite='filemanager.tests.runtests.runtests',
)
