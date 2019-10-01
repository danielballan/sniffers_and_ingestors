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

# What about the situation where the same file extension might refer to two
# different mimetypes? The mimetypes module can't handle this, but since the
# sniffers get run first, they can intercede. For example, if there is some
# other format ending in '.tiff' that is totally unrelated to the common TIFF
# serialization, we might identify it thus:
#
# def other_tiff_sniffer(filename, first_bytes):
#     SIGNAUTRE = b'SOME_SIGNAUTRE_UNLIKE_THE_COMMON_TIFF_ONE'
#     if first_bytes.startswith(SIGNATURE):
#         return 'application/x-imaginary-other-tiff-format'
#
# or, if it has no file signature, we could identify it by process of
# elimination:
#
# def other_tiff_sniffer(filename, first_bytes):
#     if filename.endswith('.tiff') and tiff_sniffer(filename, first_bytes) is None:
#         return 'application/x-imaginary-other-tiff-format'
