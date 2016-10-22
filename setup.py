from setuptools import setup

from django_redis_sentinel import __version__

description = """
Full featured redis cache backend for Django for Sentinel Redis Clusters.
"""

setup(
    name="django-redis-sentinel-redux",
    url="https://github.com/danigosa/django-redis-sentinel",
    author="Dani Gonzalez @danigosa",
    author_email="danigosa@gmail.com",
    version=__version__,
    packages=[
        "django_redis_sentinel",
        "django_redis_sentinel.client"
    ],
    description=description.strip(),
    install_requires=[
        "django-redis>=4.5.0",
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
