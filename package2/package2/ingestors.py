import functools

import h5py


def is_applicable(is_applicable_func):
    "A decorator that monkey-patches the decorated function"
    def decorator(func):
        func.is_applicable = is_applicable_func
        return func
    return decorator


def check_for_saxs(filename):
    "Used for saxs_ingestor.is_applicable"
    with h5py.File(filename, 'r') as file:
        return 'saxs_data' in file.keys()


@is_applicable(check_for_saxs)
def saxs_ingestor(filename):
    print("I am ingesting an HDF5 file with a saxs layout!")
    # TODO
    yield 'start', {}
    ...
