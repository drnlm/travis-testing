import cffi
import os
import array
import unittest

ffi = cffi.FFI()

ffi.cdef("""
int assign(const char* arg, int len);
int check();
int check2();
int assign2(const unsigned char* arg, int len);

""")


path = os.path.dirname(__file__)

lib = ffi.dlopen(os.path.join(path, 'test_lib', 'libtest.so'))


class TestFFI(unittest.TestCase):

    def setUp(self):
        self.data1 = b'\x01\xff\x02\xfe' * 200
        self.data2 = b'\xff\x01\xef' * 300

    def test_cast(self):
        cast_data1 = ffi.new("char[]", self.data1)
        self.assertEqual(lib.assign(cast_data1, len(self.data1)), 1)
        self.assertEqual(lib.check(), 1)
        cast_data2 = ffi.new("char[]", self.data2)
        self.assertEqual(lib.assign(cast_data2, len(self.data2)), 1)
        self.assertEqual(lib.check(), 1)

        barr = bytearray(self.data2)
        cast_barr = ffi.new("char[]", bytes(barr))
        self.assertEqual(lib.assign(cast_barr, len(self.data2)), 1)
        self.assertEqual(lib.check(), 1)

    def test_array(self):
        arrdata = array.array('c', self.data1)

        pointer = ffi.from_buffer(arrdata)
        self.assertEqual(lib.assign(pointer, len(self.data1)), 1)
        self.assertEqual(lib.check(), 1)

    def test_direct(self):
        self.assertEqual(lib.assign(self.data1, len(self.data1)), 1)
        self.assertEqual(lib.check(), 1)
        self.assertEqual(lib.assign(self.data2, len(self.data2)), 1)
        self.assertEqual(lib.check(), 1)


if __name__ == '__main__':
    unittest.main()

