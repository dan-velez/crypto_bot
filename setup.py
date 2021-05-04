from setuptools import setup, find_packages

setup(name='crypto_bot',
    version='0.1.0',
    description='A swiss army knife for automated crypto trading.',
    url='https://github.com/dan-velez/crypto-bot',
    author='Daniel Velez',
    author_email='daniel.enr.velez@gmail.com',
    license='Copyright Anikasystems',
    python_requires=">=3.6",
    packages=['crypto_bot'],
    entry_points={
        'console_scripts': ['crypto-bot=crypto_bot.__main__:main']
    },
    install_requires=['ccxt==1.43.5',
                    'pandas==1.1.5',
                    'termcolor==1.1.0'])