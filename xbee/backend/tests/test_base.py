#! /usr/bin/python
"""
test_base.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

Tests the XBeeBase superclass module for XBee API conformance.
"""
import unittest
from xbee.backend.base import XBeeBase
from xbee.tests.Fake import Serial


class TestWriteToDevice(unittest.TestCase):
    """
    XBeeBase class should properly._write binary data in a valid API
    frame to a given serial device.
    """

    def test_write(self):
        """
        _write method should write the expected data to the serial
        device
        """
        device = Serial()

        xbee = XBeeBase(device)
        xbee._write(b'\x00')

        # Check resuting state of fake device
        result_frame   = device.get_data_written()
        expected_frame = b'\x7E\x00\x01\x00\xFF'
        self.assertEqual(result_frame, expected_frame)

    def test_write_again(self):
        """
        _write method should write the expected data to the serial
        device
        """
        device = Serial()

        xbee = XBeeBase(device)
        xbee._write(b'\x00\x01\x02')

        # Check resuting state of fake device
        expected_frame = b'\x7E\x00\x03\x00\x01\x02\xFC'
        result_frame   = device.get_data_written()
        self.assertEqual(result_frame, expected_frame)

    def test_write_escaped(self):
        """
        _write method should write the expected data to the serial
        device
        """
        device = Serial()

        xbee = XBeeBase(device,escaped=True)
        xbee._write(b'\x7E\x01\x7D\x11\x13')

        # Check resuting state of fake device
        expected_frame = b'\x7E\x00\x05\x7D\x5E\x01\x7D\x5D\x7D\x31\x7D\x33\xDF'
        result_frame   = device.get_data_written()
        self.assertEqual(result_frame, expected_frame)


class TestNotImplementedFeatures(unittest.TestCase):
    """
    In order to properly use the XBeeBase class for most situations,
    it must be subclassed with the proper attributes definined. If
    this is not the case, then a NotImplemented exception should be
    raised as appropriate.
    """

    def setUp(self):
        """
        Set up a base class XBeeBase object which does not have
        api_commands or api_responses defined
        """
        self.xbee = XBeeBase(None)

    def test_build_command(self):
        """
        _build_command should raise NotImplemented
        """
        self.assertRaises(NotImplementedError, self.xbee._build_command, "at")

    def test_split_response(self):
        """
        split_command should raise NotImplemented
        """
        self.assertRaises(NotImplementedError, self.xbee._split_response, b"\x00")

    def test_shorthand(self):
        """
        Shorthand calls should raise NotImplementedError
        """
        try:
            self.xbee.at
        except NotImplementedError:
            pass
        else:
            self.fail("Shorthand call on XBeeBase base class should raise NotImplementedError")


class TestAsyncCallback(unittest.TestCase):
    """
    XBeeBase constructor should accept an optional callback function
    argument. When provided, this will put the module into a threaded
    mode, in which it will call the provided function with any API
    frame data received.

    As it would be very difficult to sanely test an asynchonous callback
    routine with a synchronous test process, proper callback behavior
    is not tested automatically at this time. Theoretically, the
    callback implementation logic is simple, but use it at your own risk.
    """

    def setUp(self):
        self.xbee = None
        self.serial = Serial()
        self.callback = lambda data: None
        self.error_callback = lambda data: None

    def tearDown(self):
        # Ensure proper thread shutdown before continuing
        self.xbee.halt()

    def test_provide_callback(self):
        """
        XBeeBase constructor should accept a callback function
        """
        self.xbee = XBeeBase(self.serial,
                             callback=self.callback,
                             error_callback=self.error_callback)


if __name__ == '__main__':
    unittest.main()
