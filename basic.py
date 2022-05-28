#    ██████╗ ██████╗ ███╗   ██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗███████╗
#   ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝██╔════╝
#   ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ███████║██╔██╗ ██║   ██║   ███████╗
#   ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║   ╚════██║
#   ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║██║ ╚████║   ██║   ███████║
#    ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

DIGITS = "0123456789"

#   ███████╗██████╗ ██████╗  ██████╗ ██████╗ 
#   ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
#   █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
#   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗
#   ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║
#   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}"
        result += f"\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#   ██████╗  ██████╗ ███████╗██╗████████╗██╗ ██████╗ ███╗   ██╗
#   ██╔══██╗██╔═══██╗██╔════╝██║╚══██╔══╝██║██╔═══██╗████╗  ██║
#   ██████╔╝██║   ██║███████╗██║   ██║   ██║██║   ██║██╔██╗ ██║
#   ██╔═══╝ ██║   ██║╚════██║██║   ██║   ██║██║   ██║██║╚██╗██║
#   ██║     ╚██████╔╝███████║██║   ██║   ██║╚██████╔╝██║ ╚████║
#   ╚═╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln  = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)                                                       

#   ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗███████╗
#   ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██╔════╝
#      ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║███████╗
#      ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║╚════██║
#      ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║███████║
#      ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝

TOKEN_INT      = "INT"
TOKEN_FLOAT    = "FLOAT"
TOKEN_PLUS     = "PLUS"
TOKEN_MINUS    = "MINUS"
TOKEN_MULTIPLY = "MULTIPLY"
TOKEN_DIVIDE   = "DIVIDE"
TOKEN_LPAREN   = "LPAREN"
TOKEN_RPAREN   = "RPAREN"



class Token:
    def __init__(self, type_, value=None):
        self.value = value
        self.type  = type_

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#   ██╗     ███████╗██╗  ██╗███████╗██████╗ 
#   ██║     ██╔════╝╚██╗██╔╝██╔════╝██╔══██╗
#   ██║     █████╗   ╚███╔╝ █████╗  ██████╔╝
#   ██║     ██╔══╝   ██╔██╗ ██╔══╝  ██╔══██╗
#   ███████╗███████╗██╔╝ ██╗███████╗██║  ██║
#   ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                        
class Lexer:
    def __init__(self, fn, text):
        self.fn           = fn
        self.text         = text
        self.pos          = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(TOKEN_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TOKEN_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TOKEN_MULTIPLY))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TOKEN_DIVIDE))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance
                return [], IllegalCharError(pos_start, self.pos, '"' + char + '"')
        return tokens, None

    def make_number(self):
        num_str = ""
        dot = 0
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot == 1: break
                num_str += "."
                dot += 1
            else:
                num_str += self.current_char
            self.advance()

        if dot == 0:
            return Token(TOKEN_INT, int(num_str))
        else:
            return Token(TOKEN_FLOAT, float(num_str))

#   ███╗   ██╗ ██████╗ ██████╗ ███████╗███████╗
#   ████╗  ██║██╔═══██╗██╔══██╗██╔════╝██╔════╝
#   ██╔██╗ ██║██║   ██║██║  ██║█████╗  ███████╗
#   ██║╚██╗██║██║   ██║██║  ██║██╔══╝  ╚════██║
#   ██║ ╚████║╚██████╔╝██████╔╝███████╗███████║
#   ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
                                           
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

#   ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗ 
#   ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
#   ██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝
#   ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗
#   ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║
#   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = 1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res = self.expr()
        return res

    def factor(self):
        tok = self.current_tok
        if tok.type in (TOKEN_INT, TOKEN_FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self):
        return self.bin_op(self.factor, (TOKEN_MULTIPLY, TOKEN_DIVIDE))

    def expr(self):
        return self.bin_op(self.term, (TOKEN_PLUS, TOKEN_MINUS))

    def bin_op(self, func, ops):
        left = func()

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left

#   ██████╗ ██╗   ██╗███╗   ██╗
#   ██╔══██╗██║   ██║████╗  ██║
#   ██████╔╝██║   ██║██╔██╗ ██║
#   ██╔══██╗██║   ██║██║╚██╗██║
#   ██║  ██║╚██████╔╝██║ ╚████║
#   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None

    return tokens, error