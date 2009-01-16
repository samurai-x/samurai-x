from array import array

SIZES = {
        8:'B',
        16:'H',
        32:'L'
        } # TODO: test these for 64bit

def make_void_array(data, format):
    """
        Return a packed representation of the data
        `data`.
        `format` is the count of bits to pack per value,
        one of 8, 16, 32.
    """
    typecode = SIZES[format]
    arr = array(typecode, data)
    assert arr.itemsize * 8 == format, "Running a 64bit system? Please file a bug."
    return arr.tostring()

