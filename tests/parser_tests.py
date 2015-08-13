import unittest
from faux_combinator.parser import Parser, ParserException

lparen_token = {'type': 'lparen', 'value': '('}
rparen_token = {'type': 'rparen', 'value': ')'}
eq_token = {'type': 'eq', 'value': '='}
dash_token = {'type': 'dash', 'value': '-'}
under_token = {'type': 'under', 'value': '_'}
  
class TestLexer(unittest.TestCase):
  def test_basic(self):
    def parser(tokens):
      p = Parser(tokens)
      p.expect('eq')
      return True

    ast = [eq_token]
    self.assertEqual(parser(ast), True)

  def test_many(self):
    def parser(tokens):
      p = Parser(tokens)
      p.expect('eq')
      p.expect('dash')
      p.expect('under')
      return True

    ast = [eq_token, dash_token, under_token]
    self.assertEqual(parser(ast), True)

  def test_maybe(self):
    def parser(tokens):
      p = Parser(tokens)
      p.expect('lparen')
      res = p.maybe(lambda: p.expect('eq'))
      p.expect('rparen')
      return res['value'] if res else True

    ast = [lparen_token, rparen_token]
    self.assertEqual(parser(ast), True,
        "can still parse basic stuff")

    ast = [lparen_token, eq_token, rparen_token]
    self.assertEqual(parser(ast), '=',
        "can parse a maybe token")

    with self.assertRaises(ParserException):
      ast = [dash_token]
      parser(ast)

  def test_one_of(self):
    def parser(tokens):
      p = Parser(tokens)
      return p.one_of(
          (lambda: p.expect('eq')), 
          (lambda: p.expect('dash')),
          (lambda: p.expect('under'))
      )['value']

    ast = [eq_token]
    self.assertEqual(parser(ast), '=',
        "can parse one_of's first case")

    ast = [dash_token]
    self.assertEqual(parser(ast), '-',
        "can parse one_of's second case")

    ast = [under_token]
    self.assertEqual(parser(ast), '_',
        "can parse one_of's third case")

    with self.assertRaises(ParserException):
      ast = [lparen_token]
      parser(ast)

  def test_any_of(self):
    def parser(tokens):
      p = Parser(tokens)
      return p.any_of(lambda: p.expect('eq')['value'])

    ast = []
    self.assertEqual(parser(ast), [],
        "can parse zero occurences")

    ast = [eq_token]
    self.assertEqual(parser(ast), ['='],
        "can parse one occurence")

    ast = [eq_token, eq_token, eq_token]
    self.assertEqual(parser(ast), ['=', '=', '='],
        "can parse many occurences")

  def test_many_of(self):
    def parser(tokens):
      p = Parser(tokens)
      return p.many_of(lambda: p.expect('eq')['value'])

    with self.assertRaises(ParserException):
      ast = []
      parser(ast)

    ast = [eq_token]
    self.assertEqual(parser(ast), ['='],
        "can parse one occurence")

    ast = [eq_token, eq_token, eq_token]
    self.assertEqual(parser(ast), ['=', '=', '='],
        "can parse many occurences")

  def test_fail(self):
    def parser(tokens):
      p = Parser(tokens)
      p.expect('anything')

    ast = []

    with self.assertRaises(ParserException):
      parser(ast)

if __name__ == '__main__':
  unittest.main()
