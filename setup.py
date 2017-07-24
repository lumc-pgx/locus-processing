from setuptools import setup

setup(
    name="locus_processing",
    version="0.0.1",
    description="Tools for working with locus definition files",
    author="Sander Bollen",
    author_email="a.h.b.bollen@lumc.nl",
    url="https://git.lumc.nl/PharmacogenomicsPipe/locus_processing",
    license="MIT",
    platforms=['any'],
    packages=["locus_processing"],
    install_requires=[
        "marshmallow>=2.13.5",
        "requests>=2.18.1"
    ],
    tests_requires=['pytest'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'License :: MIT License',
    ],
    keywords='bioinformatics'
)
