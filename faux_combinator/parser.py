class Parser:
  def __init__(self, tokens):
    tokens.append({'type': 'eof'}) # ..feels a bit like a hack
    self.tokens = tokens

  def expect(self, type):
    token = self.tokens.pop(0)
    if token['type'] == type:
      return token
    raise ParserException("invalid token type: expected {expected}, found {found}"
        .format(expected=type, found=token['type']))

  def maybe(self, rule):
    tokens = self.tokens[:]
    try:
      return rule()
    except ParserException:
      self.tokens = tokens

class ParserException(Exception):
  pass

#  def __enter__(self):
#    pass
#  def __exit__(self, type, value, traceback):
#    pass
