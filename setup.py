import setuptools

setuptools.setup(
    name="QuantumDeviceLib",
    version="0.1.0",
    url="https://github.com/myonlinecode1988/QuantumDeviceLib",

    author="Arnab Sarkar",
    author_email="arnab.sarkar@rochester.edu",

    description="An API to handle quantum gates and devices",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
