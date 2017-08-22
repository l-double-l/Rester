from setuptools import setup

setup(name='Rester',
    version='1.1.1',
    author='Markidonov Kirill',
    author_email='gmaridonov@gmail.com',
    url='https://github.com/l-double-l/Rester',
    license='LICENSE.txt',
    packages=['rester', 'testcase'],
    entry_points={
        'console_scripts':['apirunner = rester.apirunner:run']
    },
    test_suite="test",
    description='Rest API Testing',
    long_description=open('README.md').read(),
    install_requires=["requests", "PyYAML>=3.9", "xmltodict", "testfixtures"]
)
