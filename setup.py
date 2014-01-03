from setuptools import setup

setup(
    # http://pythonhosted.org/setuptools/setuptools.html
    name='miracle-acl',
    version='0.0.2',
    author='Mark Vartanyan',
    author_email='kolypto@gmail.com',

    url='https://github.com/kolypto/py-miracle',
    license='MIT',
    description='Flexible role-based authorization solution that is a pleasure to use',
    long_description=open('README.rst').read(),
    keywords=['acl', 'rbac', 'authorization'],

    packages=['miracle'],
    scripts=[],

    install_requires=[
    ],
    include_package_data=True,

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
