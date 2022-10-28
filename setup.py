import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="drs-compliance",
    version="0.0.12",
    author="Yash Puligundla",
    author_email="yasasvini.puligundla@ga4gh.org",
    packages=["compliance_suite"],
    package_data={'compliance_suite': ['config/*', 'schemas/*']},
    description="A compliance utility reporting system for drs server implementations",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/ga4gh/drs-compliance-suite",
    license='MIT',
    python_requires='>=3.8',
    install_requires=['python-json-logger==2.0.4',
                      'structlog==21.5.0',
                      'requests==2.28.1',
                      'Flask==2.2.0',
                      'Flask-HTTPAuth==4.7.0',
                      'pytest==7.1.2',
                      'pytest-cov==3.0.0'],
    entry_points='''
        [console_scripts]
        drs-compliance=compliance_suite.report_runner:main
    '''

)