import mimetypes


def tiff_sniffer(filename, first_bytes):
    SIGNATURE = b'\x49\x49\x2A\x00'
    if first_bytes.startswith(SIGNATURE):
        return 'image/tiff'
    # ...and/or potentially any other means of identifying a TIFF file...


def hdf_sniffer(filename, first_bytes):
    SIGNATURE = b'\x89HDF\r\n\x1a\n'
    if first_bytes.startswith(SIGNATURE):
        return 'application/x-hdf'
    # ...and/or potentially any other means of identifying an HDF file...

# example of registered a custom "made up" format and its file extension
mimetypes.add_type('application/x-madeup', '.madeup')
# We *could* add a sniffer for it as well, but if the file extension is
# the best way to identify it, we can just rely on mimetypes.
