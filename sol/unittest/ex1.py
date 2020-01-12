from unittest import mock

import unittest
import socket
import time


def sleep_and_execute(func):
    time.sleep(60)
    func()


def read(sock):
    data = sock.recv(4096)
    if data == '':
        raise sock.error('socket closed')
    return data


class Test_Ex1(unittest.TestCase):
    def test_sleep(self):
        with mock.patch('time.sleep') as sleep_func:
            mock_fun = mock.Mock()
            sleep_and_execute(mock_fun)

            sleep_func.assert_called_with(60)
            mock_fun.assert_called_with()

    def test_read(self):
        sock = mock.Mock()
        sock.recv.return_value = 'data'
        self.assertEqual(read(sock), 'data')

    def test_read_error(self):
        sock = mock.Mock()
        sock.recv.return_value = ''
        sock.error = ConnectionError

        with self.assertRaises(ConnectionError) as e:
            read(sock)

        self.assertEqual(str(e.exception),'socket closed')