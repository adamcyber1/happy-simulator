import pathlib

from setuptools import setup, find_packages

current_location = pathlib.Path(__file__).parent
readme = (current_location / "README.md").read_text()

setup(
    name='happysimulator',  # This is the name of your package
    version='0.1.0',  # The initial release version
    author='Vidavolta software.',
    author_email='vidavoltasoftware@gmail.com',  # Your contact email
    description='A simulation package for happiness scenarios',  # A short, one-sentence summary of the package
    long_description=readme,  # A detailed description of your package
    long_description_content_type='text/markdown',  # Type of the long description, for PyPI compatibility
    url='https://github.com/adamcyber1/happy-simulator',
    keywords=['simulator', 'happy', 'network', 'distributed', 'client', 'server', 'queue'],
    packages=find_packages(),  # Automatically find all sub-packages
    install_requires=[
        '',
        ''
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
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