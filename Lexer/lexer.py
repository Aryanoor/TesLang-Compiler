import ply.lex as lex
from Lexer.token import Token


class Lexer:
    def __init__(self, data):
        self.token = Token(data)
        self.lexer = lex.lex(object=self.token)
        self.data = data

    def run(self):
        self.lexer.input(self.data)
        toks = []
        for tok in self.lexer:
            toks.append(tok)
            # print(tok)
        self.show_in_table(toks)

    def show_in_table(self, tokens):
        headers = ["Line", "Column", "Token", "Value"]
        max_lengths = [len(header) for header in headers]

        for tok in tokens:
            LINE, TOK, VALUE, COL = str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos)

            # Update max_lengths
            max_lengths = [max(max_lengths[i], len(item)) for i, item in enumerate([LINE, COL, TOK, VALUE])]

        # Print headers
        header_line = "|"
        for header, length in zip(headers, max_lengths):
            header_line += f" {header.center(length)} |"
        print(header_line)
        print("-" * (sum(max_lengths) + 4 * len(headers)))

        # Assuming 'tokens' is a list of LexTokens
        for tok in tokens:
            line_start = self.data.rfind('\n', 0, tok.lexpos) + 1
            LINE, TOK, VALUE, COL = str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos - line_start + 1)
            print(
                f"| {LINE.strip().center(max_lengths[0])} | {COL.strip().center(max_lengths[1])} | {TOK.strip().center(max_lengths[2])} | {VALUE.strip().center(max_lengths[3])} |")
