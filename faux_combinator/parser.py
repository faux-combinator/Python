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

  def one_of(self, *rules):
    for rule in rules:
      result = self.maybe(rule)
      if result:
        return result
    raise ParserException("unable to parse one_of cases")

  def any_of(self, rule):
    tokens = []
    # I don't like python very much...
    # Gimme my "while (a = b):"... plz...
    res = self.maybe(rule)
    while res:
      tokens.append(res)
      res = self.maybe(rule)
    return tokens
  
  def many_of(self, rule):
    return [rule()] + self.any_of(rule)

class ParserException(Exception):
  pass

#  def __enter__(self):
#    pass
#  def __exit__(self, type, value, traceback):
#    pass
