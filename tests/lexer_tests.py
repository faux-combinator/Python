import unittest
from faux_combinator import lexer

eq_token = {'type': 'eq', 'value': '='}
dash_token = {'type': 'dash', 'value': '-'}
under_token = {'type': 'under', 'value': '_'}
  
class TestLexer(unittest.TestCase):
  def test_basic(self):
    rules = [
      [ r'=', 'eq' ],
    ]

    self.assertEqual(lexer.lex(rules, '='), [eq_token],
        "basic parsing works")

    self.assertEqual(lexer.lex(rules, '=='), [eq_token, eq_token],
        "can parse multiple occurences")

    self.assertEqual(lexer.lex(rules, '= ='), [eq_token, eq_token],
        "can parse multiple, space-separated occurences")

  def test_many(self):
    rules = [
      [ r'=', 'eq' ],
      [ r'-', 'dash' ],
      [ r'_', 'under' ],
    ]

    self.assertEqual(lexer.lex(rules, '='), [eq_token],
        "multiple rules can find first")

    self.assertEqual(lexer.lex(rules, '-'), [dash_token],
        "multiple rules can find second")

    self.assertEqual(lexer.lex(rules, '_'), [under_token],
        "multiple rules can find third")

    self.assertEqual(lexer.lex(rules, '=-_'), [eq_token, dash_token, under_token],
        "multiple rules can match all")
     
    self.assertEqual(lexer.lex(rules, '= - _'), [eq_token, dash_token, under_token],
        "multiple rules can match all with space separation")

  def test_capture(self):
    rules = [
      [ r'[a-z]+', 'id' ],
    ]

    self.assertEqual(lexer.lex(rules, 'abc def'), [
      {'type': 'id', 'value': 'abc'},
      {'type': 'id', 'value': 'def'},
    ], "captures values correctly")

  def test_fail(self):
    rules = []

    with self.assertRaises(lexer.LexerException):
      lexer.lex(rules, 'anything')

if __name__ == '__main__':
  unittest.main()
