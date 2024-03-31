from Lexer.lexer import Lexer
from Lexer.token import Token

if __name__ == '__main__':

    data = """
    <% Here Is A Comment %>
    fn sum(a as int, b as int) <int>
    begin
        result :: int = 0;
        result = a + b;
        return result
    end
"""
    tok = Token(data)
    lexer = Lexer(tok)
    lexer.build(data)