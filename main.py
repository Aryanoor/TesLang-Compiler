from Lexer.lexer import *
from Parser.parser import *
from Parser.semanticChecker import SemanticChecker
from Parser.pre_parser import *

if __name__ == '__main__':
    with open('Teslang Codes/sample3.teslang', 'r') as file:
        data10 = file.read()

    lexer = myLex(data10)  # Ensure lexer is correctly initialized
    parser = yacc.yacc()  # Use parser with correct module configuration
    ast = parser.parse(data10, lexer=lexer, debug=True, tracking=True)

    try:
        ast_root = PreParser().visit(ast)
    except Exception as e:
        print(f"Error during pre-parsing: {e}")

    checker = SemanticChecker()
    checker.visit(ast_root)
