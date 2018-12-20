from tyr.lexer import *
import unittest

class TestConsolidate(unittest.TestCase):
  def setUp(self):
    from random import Random
    self.random = Random(42)

  def test_consolidate_char(self):
    for i in range(2*26):
      char = chr(i + ord('a')) if i < 26 else chr(i - 26 + ord('A'))
      with self.subTest(char=char):
        self.assertEqual(Token("_CHAR", 1, char, char).consolidate(), char)
    for char in ['\\n', '\\\\']:
      with self.subTest(char=char):
        self.assertEqual(Token("_CHAR", 2, char, char).consolidate(), char)

if __name__ == "__main__":
  unittest.main()
