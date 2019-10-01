import h5py
import numpy
import tifffile


def main():
    # some good examples
    with h5py.File('tomo_example.h5', 'w') as file:
        file['tomo_data'] = numpy.ones((100, 100))
    with h5py.File('saxs_example.h5', 'w') as file:
        file['saxs_data'] = numpy.ones((100, 100))
    tifffile.imsave('example_plane.tiff', numpy.ones((100, 100)))
    tifffile.imsave('example_stack.tiff', numpy.ones((5, 100, 100)))
    with open('tabular_data.csv', 'w') as file:
        file.write('a,b,c\r\n1,2,3\r\n4,5,6')
    with open('custom_format_example.madeup', 'wb') as file:
        file.write(b'beepboop')

    # some edge cases
    with h5py.File('confounding_example.h5', 'w') as file:
        file['saxs_data'] = numpy.ones((100, 100))
        file['tomo_data'] = numpy.ones((100, 100))
    with open('garbled_file.tiff', 'wb') as file:
        file.write(b'jibberish_jibberish_jibberish')

if __name__ == '__main__':
    main()
