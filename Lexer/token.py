
class Token:

    def __init__(self, text):
        self.message = text

    # List of token names
    tokens = (
        'FN', 'RETURN', 'NULL_TYPE', 'AS', 'BEGIN', 'END', 'TO',
        'LPAREN', 'RPAREN', 'LCURLYBR', 'RCURLYBR', 'LBRACKET', 'RBRACKET', 'SEMI_COLON', 'COLON', 'COMMA', 'DBL_COLON',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'AND', 'OR', 'NOT', 'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL',
        'FOR_LOOP', 'WHILE_LOOP',
        'IF', 'ELSE',
        'INT_TYPE', 'STR_TYPE', 'VECTOR_TYPE',
        'COMMENT', 'ENTER',
        'NUMBER', 'IDENTIFIER'
    )

    # Regex Rules For Simple Tokens
    ##KEYWOARDS:
    t_FN = r'fn'
    t_RETURN = r'return'
    t_NULL_TYPE = r'null'
    t_AS = r'as'
    t_BEGIN = r'begin'
    t_END = r'end'
    t_TO = r'to'

    ##Punctuation and Delimiters:
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURLYBR = r'{'
    t_RCURLYBR = r'}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_SEMI_COLON = r';'
    t_COLON = r':'
    t_DBL_COLON = r'::'
    t_COMMA = r','

    ##ARITHMATIC OPERATORS:
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'

    ##LOGICAL OPERATORS:
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_ASSIGN = r'='
    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_LESS_THAN = r'<'
    t_LESS_THAN_EQUAL = r'<='
    t_GREATER_THAN = r'>'
    t_GREATER_THAN_EQUAL = r'>='

    ##LOOPS:
    t_FOR_LOOP = r'for'
    t_WHILE_LOOP = r'while'

    ##CONDITIONS:
    t_IF = r'if'
    t_ELSE = r'while'

    ##DATA TYPES:
    t_INT_TYPE = r'int'
    t_STR_TYPE = r'str'
    t_VECTOR_TYPE = r'vector'

    t_ignore = ' \t'

    #  Regular expression rule with some action code

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t


    def t_COMMENT(self, t):
        r'<%(.)*%>'
        return

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'

        keywords = {
            'fn': 'FN',
            'as': 'AS',
            'begin': 'BEGIN',
            'end': 'END',
            'int': 'INT_TYPE',
            'vector': 'VECTOR_TYPE',
            'str': 'STR_TYPE',
            'null': 'NULL_TYPE',
            'var': 'VAR',
            'return': 'RETURN',
            'for': 'FOR_LOOP',
            'while': 'WHILE_LOOP',
            'if': 'IF',
            'else': 'ELSE',
            'to': 'TO'
        }

        t.type = keywords.get(t.value, 'IDENTIFIER')
        return t

    # This function is defined to handle errors that occur during tokenization.
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)