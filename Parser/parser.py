import ply.yacc as yacc
from Lexer.lexer import myLex
from Parser.AST import *


def find_position(p, token_index):
    """
    Finds the position (line number) of a token in the parsing context.

    Args:
        p: The parsing context from PLY.
        token_index: Index of the token in the parsing rule.

    Returns:
        The line number of the token.
    """
    return p.lineno(token_index)


def p_prog(p):
    '''prog : func prog
            | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_func(p):
    '''func : FN IDENTIFIER LPAREN flist RPAREN LESS_THAN type GREATER_THAN LCURLYBR body RCURLYBR
            | FN IDENTIFIER LPAREN flist RPAREN LESS_THAN type GREATER_THAN ARROW RETURN expr SEMI_COLON'''
    if len(p) == 12:
        p[0] = FunctionDefinition(name=p[2], params=p[4], return_type=p[7], body=p[10], pos=find_position(p, 1))
    elif len(p) == 14:
        p[0] = FunctionDefinition(name=p[2], params=p[4], return_type=p[7], body=[Return(expr=p[12])], pos=find_position(p, 1))


def p_stmt(p):
    '''stmt : expr SEMI_COLON
            | defvar SEMI_COLON
            | func
            | IF LBRACKET expr RBRACKET stmt
            | IF LBRACKET expr RBRACKET stmt ELSE stmt
            | WHILE_LOOP LBRACKET expr RBRACKET stmt
            | DO stmt WHILE_LOOP LBRACKET expr RBRACKET SEMI_COLON
            | FOR_LOOP LPAREN IDENTIFIER ASSIGN expr TO expr RPAREN stmt
            | BEGIN body END
            | RETURN expr SEMI_COLON'''
    p[0] = p[1]  # Just set the result to the first production, actual handling depends on AST structure


def p_expr(p):
    '''expr : expr LBRACKET expr RBRACKET
            | LBRACKET clist RBRACKET
            | expr QUESTION_MARK expr COLON expr
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr GREATER_THAN expr
            | expr LESS_THAN expr
            | expr EQUAL expr
            | expr GREATER_THAN_EQUAL expr
            | expr LESS_THAN_EQUAL expr
            | expr NOT_EQUAL expr
            | expr OR expr
            | expr AND expr
            | NOT expr
            | PLUS expr
            | MINUS expr
            | IDENTIFIER
            | IDENTIFIER ASSIGN expr
            | IDENTIFIER LPAREN clist RPAREN
            | NUMBER'''
    if len(p) == 4:
        p[0] = BinaryOp(p[1], p[2], p[3], find_position(p, 1))
    elif len(p) == 3:
        p[0] = UnaryOp(p[1], p[2], find_position(p, 1))
    else:
        p[0] = p[1]


def p_flist(p):
    '''flist : empty
             | param_decl
             | param_decl COMMA flist'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]


def p_clist(p):
    '''clist : expr
             | expr COMMA clist'''
    if len(p) == 2:
        p[0] = [p[1]]  # Single expression in the list
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]  # Concatenate the first expression with the rest of the list


def p_param_decl(p):
    '''param_decl : IDENTIFIER AS type'''
    p[0] = Parameter(p[1], p[3], find_position(p, 1))


def p_type(p):
    '''type : INT_TYPE
            | STR_TYPE
            | VECTOR_TYPE
            | BOOL_TYPE'''


def p_body(p):
    '''body : statement_list'''
    p[0] = Body(p[1], find_position(p, 1))


def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_statement(p):
    '''statement : expr SEMI_COLON
                 | defvar SEMI_COLON
                 | func
                 | RETURN expr SEMI_COLON
                 | IF LBRACKET expr RBRACKET stmt
                 | IF LBRACKET expr RBRACKET stmt ELSE stmt
                 | WHILE_LOOP LBRACKET expr RBRACKET stmt
                 | DO stmt WHILE_LOOP LBRACKET expr RBRACKET SEMI_COLON
                 | FOR_LOOP LPAREN IDENTIFIER ASSIGN expr TO expr RPAREN stmt
                 | BEGIN body END'''
    p[0] = p[1]  # Just set the result to the first production


def p_defvar(p):
    '''defvar : IDENTIFIER DBL_COLON type
              | IDENTIFIER DBL_COLON type ASSIGN expr'''
    if len(p) == 4:
        p[0] = VariableDeclaration(p[1], p[3], None, find_position(p, 1))
    elif len(p) == 6:
        p[0] = VariableDeclaration(p[1], p[3], p[5], find_position(p, 1))


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")


# if __name__ == '__main__':
#     parser = yacc.yacc()
#     with open('../Teslang Codes/sample3.teslang', 'r') as file:
#         data1 = file.read()
#
#     my_lexer = myLex(data1)
#
#     ast = parser.parse(data1, tracking=True, lexer=my_lexer)
#     checker = SemanticChecker()
#     checker.visit(ast)