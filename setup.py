from setuptools import setup, find_packages
import re


version = ''
with open('engel/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')


readme = 'See https://github.com/Dalloriam/engel for README.'

setup(
    name='engel',
    author='Dalloriam',
    author_email='dalloriam@gmail.com',
    url='https://github.com/Dalloriam/engel',
    version=version,
    packages=find_packages(),
    license='MIT',
    description='Build rock-solid web interfaces for your projects.',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    long_description=readme,
    package_data={'engel': ['index.html', 'engeljs.js'], 'eng': ['templates/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'eng=eng.eng_cli:main'
        ]
    },
    install_requires=[
        "autobahn==0.13.0",
        "requests==2.10.0",
        "asyncio==3.4.3",
        "colorama==0.3.7",
        "Jinja2"
    ]
)
