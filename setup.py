from setuptools import setup, find_packages

VERSION = '0.1.4'

setup(
    name='seqtolang',
    version=VERSION,
    description="Multi Langauge Documents Langauge identification",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hiredscorelabs/seqtolang",
    keywords='Deep Learning Natural Language Processing NLP Machine Learning',
    license='Apache',
    packages=find_packages(exclude=['test*']),
    package_data={'seqtolang': ['checkpoints/*.*']},
    include_package_data=True,
    install_requires=[
        'torch>=1.1.0',
    ],
)
