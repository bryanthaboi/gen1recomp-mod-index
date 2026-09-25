"""Parse cartkit's data-only Lua table format without a Lua interpreter."""
import re


def parse_bundle(raw):
    if len(raw) > 8 * 1024 * 1024: raise ValueError('Cart manifest exceeds size limit')
    text = raw.decode('utf-8-sig')
    pos, tokens = 0, 0

    def whitespace():
        nonlocal pos
        while pos < len(text) and text[pos].isspace(): pos += 1

    def take(expected):
        nonlocal pos
        whitespace()
        if not text.startswith(expected, pos): raise ValueError('Invalid data-only cart syntax')
        pos += len(expected)

    def value(depth=0):
        nonlocal pos, tokens
        whitespace(); tokens += 1
        if depth > 64 or tokens > 200000: raise ValueError('Cart nesting or field limit exceeded')
        if pos >= len(text): raise ValueError('Truncated cart')
        char = text[pos]
        if char in ('"', "'"):
            pos += 1; out = []
            while pos < len(text):
                c = text[pos]; pos += 1
                if c == char: return ''.join(out)
                if c == '\\':
                    if pos >= len(text): raise ValueError('Truncated string')
                    match = re.match(r'\d{1,3}', text[pos:])
                    if match:
                        code = int(match[0])
                        if code > 255: raise ValueError('Invalid byte escape')
                        out.append(chr(code)); pos += len(match[0]); continue
                    c = text[pos]; pos += 1
                    escapes = {'n': '\n', 'r': '\r', 't': '\t', '\\': '\\', '"': '"', "'": "'", '\n': '\n'}
                    if c not in escapes: raise ValueError('Unsupported cart escape')
                    c = escapes[c]
                out.append(c)
            raise ValueError('Unterminated cart string')
        if char == '{':
            pos += 1; table = {}; index = 1
            while True:
                whitespace()
                if pos < len(text) and text[pos] == '}':
                    pos += 1
                    if table and set(table) == set(range(1, len(table) + 1)):
                        return [table[n] for n in range(1, len(table) + 1)]
                    return table
                if text.startswith('[', pos):
                    pos += 1; key = value(depth + 1); take(']'); take('=')
                else:
                    match = re.match(r'([A-Za-z_]\w*)\s*=', text[pos:])
                    if match: key = match[1]; pos += len(match[0])
                    else: key = index; index += 1
                if not isinstance(key, (str, int)) or key in table: raise ValueError('Invalid or duplicate cart key')
                table[key] = value(depth + 1)
                whitespace()
                if pos < len(text) and text[pos] in ',;': pos += 1
                elif pos >= len(text) or text[pos] != '}': raise ValueError('Cart separator missing')
        for literal, decoded in [('true', True), ('false', False)]:
            if text.startswith(literal, pos): pos += len(literal); return decoded
        match = re.match(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', text[pos:])
        if match:
            pos += len(match[0]); return float(match[0]) if any(c in match[0] for c in '.eE') else int(match[0])
        raise ValueError('Executable or unsupported expression in cart')

    take('return')
    bundle = value()
    whitespace()
    if pos != len(text) or not isinstance(bundle, dict) or bundle.get('format') != 'g1rcart' or bundle.get('formatVersion') != 1:
        raise ValueError('Unsupported cart format or trailing executable content')
    if not isinstance(bundle.get('cart'), dict): raise ValueError('Cart data missing')
    if set(bundle) - {'format', 'formatVersion', 'cart', 'labelArt'}: raise ValueError('Unknown bundle fields')
    return bundle
