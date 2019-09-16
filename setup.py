from setuptools import setup, find_packages

install_requires = open("requirements.txt").read().splitlines()

setup(
    name="django-graphql-ratelimit",
    version="1.0.1",
    description="Use django-ratelimit for graphql",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="o3o3o",
    author_email="o3o3o.me@gmail.com",
    url="https://github.com/o3o3o/django-graphql-ratelimit",
    license="Apache Software License",
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
