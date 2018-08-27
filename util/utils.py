import os


def set_io_dir(input, output):
    if not os.path.isdir(input):
        raise IOError(input, 'not found')

    if not os.path.isdir(output):
        os.makedirs(output)

    return input, output
