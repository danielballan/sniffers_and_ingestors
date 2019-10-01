from setuptools import setup


setup(
    name='package1',
    packages=['package1'],
    entry_points={
       'databroker.sniffers': [
           'image/tiff = package1.sniffers:tiff_sniffer',
           'application/x-hdf = package1.sniffers:hdf_sniffer',
       ],
       'databroker.ingestors': [
           'image/tiff = package1.ingestors:tiff_ingestor',
           'text/csv= package1.ingestors:csv_ingestor',
           'application/x-hdf= package1.ingestors:tomo_ingestor',
           'application/x-madeup= package1.ingestors:madeup_format_ingestor',
        ]},
    )

