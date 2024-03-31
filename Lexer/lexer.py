import ply.lex as lex


class Lexer:
    def __init__(self, tokens):
        self.lexer = lex.lex(object=tokens)

    def run(self, data):
        self.lexer.input(data)
        toks = []
        for tok in self.lexer:
            toks.append(tok)
        show_in_table(toks)


def show_in_table(tokens):
    headers = ["Line", "Column", "Token", "Value"]
    max_lengths = [len(header) for header in headers]

    for tok in tokens:
        items = str(tok)[9:-1].split(",")
        LINE, COL, TOK, VALUE = items[2], items[3], items[0], items[1]

        # Update max_lengths
        max_lengths = [max(max_lengths[i], len(item)) for i, item in enumerate([LINE, COL, TOK, VALUE])]

    # Print headers
    header_line = "|"
    for header, length in zip(headers, max_lengths):
        header_line += f" {header.center(length)} |"
    print(header_line)
    print("-" * (sum(max_lengths) + 5 * len(headers)))

    # Assuming 'tokens' is a list of LexTokens
    for tok in tokens:
        items = str(tok)[9:-1].split(",")
        if items[0] == "COMMA":
            TOK, VALUE, LINE, COL = items[0], "','", items[3], items[4]

        else:
            LINE, COL, TOK, VALUE = items[2], items[3], items[0], items[1]
        print(
            f"| {LINE.strip().center(max_lengths[0])} | {COL.strip().center(max_lengths[1])} | {TOK.strip().center(max_lengths[2])} | {VALUE.strip().center(max_lengths[3])} |")
