import pathlib

from setuptools import setup, find_packages

current_location = pathlib.Path(__file__).parent
readme = (current_location / "README.md").read_text()

setup(
    name='happysimulator',
    version='0.1.0',
    author='VidaVolta software.',
    author_email='vidavoltasoftware@gmail.com',
    description='Simulate, visualize, and understand systems with easy to build simulation.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/adamcyber1/happy-simulator',
    keywords=['simulator', 'happy', 'network', 'distributed', 'client', 'server', 'queue'],
    packages=find_packages(),
    install_requires=[
        '',
        ''
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.7'
)