from Lexer.lexer import Lexer

if __name__ == '__main__':
    with open('TesLang Codes/sample1.teslang', 'r') as file:
        data = file.read()

    program = Lexer(data)
    program.run()