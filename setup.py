from distutils.core import setup

setup(
    name='miracle',
    version='0.0.1',
    author='Mark Vartanyan',
    author_email='kolypto@gmail.com',

    url='http://pypi.python.org/pypi/miracle/',
    license='LICENSE.txt',
    description='Flexible role-based authorization solution that is a pleasure to use',
    long_description=open('README.rst').read(),
    keywords=['acl', 'rbac', 'authorization'],

    packages=['miracle','miracle.testsuite'],
    scripts=[],

    install_requires=[
    ],
    include_package_data=True,
    test_suite='miracle.testsuite.suite',

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent'
    ],
)
