def sizeof_fmt(num):
    """
    Format file sizes for a humans beings.
    http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def generate_breadcrumbs(path):
    parts = path.rsplit('/', 1)

    if path is None or len(path) == 0:
        return []

    result = [{
        'label': parts[-1],
        'path': path,
    }]

    if len(parts) == 2:  # there are some more slashes
        return generate_breadcrumbs(parts[0]) + result
    return result
