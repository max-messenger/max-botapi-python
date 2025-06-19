from setuptools import setup, find_packages

setup(
    name="maxapi",
    version="0.1",
    packages=find_packages(),
    description="Библиотека для взаимодействия с API мессенджера MAX",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Денис",
    url="https://github.com/love-apples/maxapi/tree/main",
    install_requires=[
        'aiohttp==3.11.16',
        'fastapi==0.115.13',
        'magic_filter==1.0.12',
        'pydantic==2.11.7',
        'uvicorn==0.34.3'
    ],
    python_requires=">=3.10",
)