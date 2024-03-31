import ply.lex as lex


class Lexer:
    def __init__(self, tokens):
        self.lexer = lex.lex(object=tokens)

    def build(self, data):
        self.lexer.input(data)
        toks = []
        for tok in self.lexer:
            toks.append(tok)
            print(tok)
