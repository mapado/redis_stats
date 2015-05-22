from setuptools import setup, find_packages

setup(
    name="redis_stats",
    version='0.1.0',
    description='Some stats about Redis',
    maintainer="Julien Deniau",
    maintainer_email='julien.deniau@mapado.com',
    packages=find_packages(),
    install_requires=[
        'redis>=2.0.0,<3.0.0',
        'scikit-learn>=0.16.0,<0.17.0',
    ],
 )

