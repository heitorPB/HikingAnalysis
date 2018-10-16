from setuptools import setup

setup(
    name='Hiking Analysis',
    version='0.1',
    url="https://github.com/heitorPB/HikingAnalysis",
    author="Heitor de Bittencourt",
    description="A package to get statistics and plots from a GPX file",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hikingAnalysis=hikingAnalysis.main:cli
    ''',
)
