""""Tests for the roman numerals module"""
import unittest
from hypothesis import given, example
from hypothesis.strategies import integers


from sol.games.roman_numerals import toroman


class Test_RomanNumerals(unittest.TestCase):
    """Test roman_numerals.py"""

    def test_invalid_input_type(self):
        """Tests an invalid input type"""
        with self.assertRaises(TypeError):
            toroman('123')
        with self.assertRaises(TypeError):
            toroman(1.3)
        with self.assertRaises(TypeError):
            toroman([1])
        with self.assertRaises(TypeError):
            toroman((1))

    @given(integers(min_value=0))
    @example(0)
    @example(10)
    @example(100)
    def test_valid_input(self, num):
        """Tests valid inputs"""
        self.assertEqual(self._fromroman(toroman(num)), num)

    def _fromroman(num):
        pass


if __name__ == '__main__':
    unittest.main()
