import mimetypes
import warnings

import entrypoints


def ingest_file(filename):
    """
    Take in a file name; return a generator that yields (name, doc) pairs.
    """
    mimetype = detect_mimetype(filename)
    ingestor = choose_ingestor(filename, mimetype)
    generator_instance = ingestor(filename)
    return generator_instance


def detect_mimetype(filename):
    """
    Take in a filename; return a mimetype string like 'image/tiff'.
    """
    # First rely on custom "sniffers" that can employ file signatures (magic
    # numbers) or any other format-specific tricks to extract a mimetype.
    with open(filename, 'rb') as file:
        # The choice of 64 bytes is arbitrary. We may increase this in the
        # future if we discover reason to. Therefore, sniffers should not
        # assume that they will receive this exact number of bytes.
        first_bytes = file.read(64)
    for ep in entrypoints.get_group_all('databroker.sniffers'):
        content_sniffer = ep.load()
        mimetype = content_sniffer(filename, first_bytes)
        if mimetype is not None:
            return mimetype
            # TODO Instead of bailing when we get the first match, we might
            # keep going to check for *conflicting* assessments and warn if
            # that happens.
    else:
        # None of the sniffers found a match. Fall back to guessing based on
        # file extension.
        mimetype, _ = mimetypes.guess_type(filename)
        if mimetype is None:
            raise UnknownFileType(f"Could not identify the MIME type of {filename}")
        return mimetype


def applicable_ingestors(filename, mimetype):
    """
    Take in a filename and its mimetype; return a list of compatible ingestors.
    """
    # Find ingestor(s) for this mimetype.
    ingestors = []
    for ep in entrypoints.get_group_all('databroker.ingestors'):
        if ep.name == mimetype:
            ingestors.append(ep.load())
    # Let each ingestor look at the content of this file and decide if it
    # thinks it can handle it. An ingestor *may* implement 'is_applicable' to
    # do this. If it does not implement 'is_applicable', it is assumed to be
    # suitable for *all* files of this mimetype.
    for ingestor in list(ingestors):
        if hasattr(ingestor, 'is_applicable'):
            if not ingestor.is_applicable(filename):
                ingestors.remove(ingestor)
    return ingestors


def choose_ingestor(filename, mimetype):
    """
    Take in a filename and its mimetype; return an ingestor.

    If multiple are found, return the first one (deterministic but arbitrary).
    If none are found, raise.
    """
    ingestors = applicable_ingestors(filename, mimetype)
    if not ingestors:
        raise NoIngestor(f"No ingestors were applicable to {filename}")
    elif len(ingestors) > 1:
        warnings.warn("More than one ingestor was applicable.")
    return ingestors[0]


class UnknownFileType(ValueError):
    ...


class NoIngestor(ValueError):
    ...
