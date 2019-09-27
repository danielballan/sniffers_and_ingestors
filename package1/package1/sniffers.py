def tiff_sniffer(filename):
    SIGNATURE = b'\x49\x49\x2A\x00'
    with open(filename, 'rb') as file:
        if file.read(64).startswith(SIGNATURE):
            return 'image/tiff'
    # ...and/or potentially any other means of identifying a TIFF file...


def hdf_sniffer(filename):
    SIGNATURE = b'\x89HDF\r\n\x1a\n'
    with open(filename, 'rb') as file:
        if file.read(64).startswith(SIGNATURE):
            return 'application/x-hdf'
    # ...and/or potentially any other means of identifying an HDF file...
