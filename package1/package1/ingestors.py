import functools

import h5py
import tifffile


def ingest_plane(filename):
    print("I am ingesting a tiff plane!")
    # TODO ...
    yield 'start', {}
    ...
    


def ingest_stack(filename):
    print("I am ingesting a tiff stack!")
    # TODO ...
    yield 'start', {}
    ...
    

def tiff_ingestor(filename):
    """
    This is registered for the 'image/tiff' mimetype.

    It is applicable for all known 'image/tiff' files.
    """
    if tifffile.imread(filename).ndim == 2:
        yield from ingest_plane(filename)
    if tifffile.imread(filename).ndim == 3:
        yield from ingest_stack(filename)


def is_applicable(is_applicable_func):
    "A decorator that monkey-patches the decorated function"
    def decorator(func):
        func.is_applicable = is_applicable_func
        return func
    return decorator


def check_for_tomo(filename):
    "Used for tomo_ingestor.is_applicable"
    with h5py.File(filename, 'r') as file:
        return 'tomo_data' in file.keys()


@is_applicable(check_for_tomo)
def tomo_ingestor(filename):
    print("I am ingesting an HDF5 file with a tomo layout!")
    # TODO
    yield 'start', {}
    ...
