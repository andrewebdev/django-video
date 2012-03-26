from setuptools import setup, find_packages

setup(
    name="videodemo",
    version="0.1",
    url="",
    description="A demo project for django-video tests etc.",
    author="Andre Engelbrecht",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
    ],
)
