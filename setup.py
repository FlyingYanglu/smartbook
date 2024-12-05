from setuptools import setup

setup(
    name='smartbook',
    version='0.0.1',
    description='Visual Novel Generator',
    author='HY YC',
    author_email='',
    url='',
    packages=['smartbook'],
    install_requires=[
        'natsort',
        'tqdm',
        'openai',
        'influxdb',
        'flask',
        'celery',
        'redis',
        'PoePT @ git+https://github.com/FlyingYanglu/PoePT@main#egg=PoePT',  # Add GitHub dependency
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
