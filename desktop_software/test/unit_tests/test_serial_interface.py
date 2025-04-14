import unittest

from src.framework.serial_interface_exception import SerialInterfaceException
from src.serial_interface.serial_interface_impl import SerialInterfaceImpl


class ScoreBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.fixture = SerialInterfaceImpl("COM5",9600)

    def tearDown(self):
        if self.fixture.is_open():
            self.fixture.close()
        del self.fixture

    def test_fixture_exists(self):
        self.assertIsNotNone(self.fixture)

    def test_should_throw_if_not_open(self):
        self.assertRaises(SerialInterfaceException, self.fixture.read_note_data)

    def test_should_not_throw_if_open(self):
        self.fixture.open()
        self.assertIsNotNone(self.fixture.read_note_data())


if __name__ == '__main__':
    unittest.main()
