import unittest
from faux_combinator import lexer

eq_token = {'type': 'eq', 'value': '='}
  
class TestLexer(unittest.TestCase):
  def test_basic(self):
    rules = [
      [ r'=', 'eq' ]
    ]
    self.assertEqual(lexer.lex(rules, '='), [eq_token],
        'can parse basic stuff')

if __name__ == '__main__':
  unittest.main()
