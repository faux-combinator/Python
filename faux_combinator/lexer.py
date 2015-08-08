import re
base_regexp = "^(%s)"

def lex(rules, code):
  tokens = []
  while code:
    code = code.lstrip(' \t')
    for rule in rules:
      pattern, type = rule
      result = re.search(base_regexp % pattern, code)
      if result:
        value = result.group(1)
        tokens.append({'type': type, 'value': value})
        code = code[len(value):]
        break
  return tokens
