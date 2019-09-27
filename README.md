# Example ingestors

There are two interfaces. Functions registered as ``'databroker.sniffers'``
must accept a filename (filenames?) and return a mimetype or None.

```python
def sniifer(filename):
    if ...:
        return 'some_mimetype'
    # Implicitly return None if we don't recognize this file.
```

Functions registered as ``'databroker.ingestors'`` must accept a filename
(filenames?) and return a generator instance that yields ``(name, doc)`` pairs.

```python
def ingestor(filename):
    ...
    yield name, doc
    ...
```

The ingestor may, internally, examine the file strucutre (e.g. TIFF plane vs stack) and
dispatch out to other functions, but that's an internal detail up the
implementation. Additionally, functions registered as ``'databroker.ingestors'``
MAY implement an attribute ``is_applicable``. If implemented, it must accept a
filename (filenames?) and return a boolean.

```python
ingestor.is_applicable(filename)
```

That's the complete public interface.

Here is a runnable example. It includes:

* a script for generating example data files
* ``ingest.py``, providing the "user API" that might go into databroker
* ``package1`` which provides some sniffers and ingestors for TIFF and HDF5
* ``package2`` which provides another ingestor for HDF5

```
$ python generate_example_files.py
$ pip install -e package1/
$ pip install -e package2/
```

```py
In [1]: import ingest                                                                                                                                                                         

In [2]: gen = ingest.ingest_file('example_plane.tiff')                                                                                                                                        

In [3]: next(gen)                                                                                                                                                                             
I am ingesting a tiff plane!
Out[3]: ('start', {})

In [4]: gen = ingest.ingest_file('example_stack.tiff')                                                                                                                                        

In [5]: next(gen)                                                                                                                                                                             
I am ingesting a tiff stack!
Out[5]: ('start', {})

In [6]: gen = ingest.ingest_file('tomo_example.h5')                                                                                                                                           

In [7]: next(gen)                                                                                                                                                                             
I am ingesting an HDF5 file with a tomo layout!
Out[7]: ('start', {})

In [8]: gen = ingest.ingest_file('saxs_example.h5')                                                                                                                                           

In [9]: next(gen)                                                                                                                                                                             
I am ingesting an HDF5 file with a saxs layout!
Out[9]: ('start', {})

In [10]: gen = ingest.ingest_file('confounding_example.h5')                                                                                                                                   
/home/dallan/Repos/bnl/sniffers_and_ingestors/ingest.py:62: UserWarning: More than one ingestor was applicable.
  warnings.warn("More than one ingestor was applicable.")

In [11]: next(gen)                                                                                                                                                                            
I am ingesting an HDF5 file with a saxs layout!
Out[11]: ('start', {})
```

This example includes two packages, creatively named ``package1`` and
``package2``. Notice that:

* Both package1 and package2 register ways of handling HDF5 files. They do not
  shadow each other unless they are given a file that *both* think they can
  handle (``'confounding_example.h5``). In that case, the first one wins.
* The logic for identifying the MIME type is separated the rest. In fact,
  package2 doesn't have any file-type-identifying logic. The author of package2
  doesn't need to know about file signature or worry about possible file
  extneions. They just write a function that knows it will receive an HDF5 file
  and goes from there.
