from setuptools import setup


setup(
    name='package2',
    packages=['package2'],
    entry_points={
       'databroker.ingestors': [
           'application/x-hdf= package2.ingestors:saxs_ingestor',
        ]},
    )

