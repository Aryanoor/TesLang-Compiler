class Token:

    def __init__(self, text):
        """
            Initializes a Token object with the given text.

            Parameters:
                text (str): The text content of the token.
        """
        self.message = text

    # List of token names
    tokens = (
        'FN', 'RETURN', 'NULL_TYPE', 'AS', 'BEGIN', 'END', 'TO', 'SCAN', 'PRINT', 'LIST', 'LENGTH', 'EXIT',
        'LPAREN', 'RPAREN', 'LCURLYBR', 'RCURLYBR', 'LBRACKET', 'RBRACKET', 'SEMI_COLON', 'COLON', 'COMMA', 'DBL_COLON',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'AND', 'OR', 'NOT', 'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN',
        'GREATER_THAN_EQUAL',
        'FOR_LOOP', 'WHILE_LOOP',
        'IF', 'ELSE',
        'INT_TYPE', 'STR_TYPE', 'VECTOR_TYPE', 'BOOL_TYPE', 'SINGLE_QT', 'DBL_QT',
        'COMMENT', 'ENTER',
        'NUMBER', 'IDENTIFIER'
    )

    # Regex Rules For Simple Tokens
    ##KEYWOARDS:
    # Define regular expressions for keywords and assign token names to them
    t_FN = r'fn'
    t_RETURN = r'return'
    t_NULL_TYPE = r'null'
    t_AS = r'as'
    t_BEGIN = r'begin'
    t_END = r'end'
    t_TO = r'to'
    t_SCAN = r'scan'
    t_PRINT = r'print'
    t_LIST = r'list'
    t_LENGTH = r'length'
    t_EXIT = r'exit'

    ##Punctuation and Delimiters:
    # Define regular expressions for punctuation and delimiters and assign token names to them
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
    # Define regular expressions for arithmetic operators and assign token names to them
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'

    ##LOGICAL OPERATORS:
    # Define regular expressions for logical operators and assign token names to them
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
    # Define regular expressions for loop keywords and assign token names to them
    t_FOR_LOOP = r'for'
    t_WHILE_LOOP = r'while'

    ##CONDITIONS:
    # Define regular expressions for conditional keywords and assign token names to them
    t_IF = r'if'
    t_ELSE = r'else'

    ##DATA TYPES:
    # Define regular expressions for data type keywords and assign token names to them
    t_INT_TYPE = r'int'
    t_STR_TYPE = r'str'
    t_VECTOR_TYPE = r'vector'
    t_BOOL_TYPE = r'boolean'

    t_ignore = ' \t'

    #  Regular expression rule with some action code
    def t_newline(self, t):
        # Handles newline characters in the input.
        #
        # Parameters:
        #      t (LexToken): The token object.
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t):
        # Matches numerical literals.
        #
        # Parameters:
        #     t (LexToken): The token object.
        #
        # Returns:
        #     LexToken: The token object with updated value.
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_SINGLE_QT(self, t):
        r"[']"
        depth = 1
        my_string = ""

        while depth > 0:
            next_char = t.lexer.lexdata[t.lexer.lexpos]
            if next_char == "'":
                print(my_string)
                depth -= 1
            if next_char == '\n':
                t.lexer.lineno += 1
            my_string += next_char
            t.lexer.lexpos += 1
        t.value = my_string
        return t

    def t_DBL_QT(self, t):
        r'["]'
        depth = 1
        my_string = ""

        while depth > 0:
            next_char = t.lexer.lexdata[t.lexer.lexpos]
            if next_char == '"':
                print(my_string)
                depth -= 1
            if next_char == '\n':
                t.lexer.lineno += 1
            my_string += next_char
            t.lexer.lexpos += 1
        t.value = my_string
        return t

    def t_COMMENT(self, t):
        r'<%'  # This regex triggers the start of a comment in the lexer.
        comment_depth = 1  # Initialize depth counter to handle nested comments.
        t.lexer.comment_start = t.lexer.lexpos  # Store the position where the comment starts.

        # Continue parsing until all comment blocks are properly closed.
        while comment_depth > 0:
            next_char = t.lexer.lexdata[t.lexer.lexpos]  # Get the current character at lexer's position.

            # Check if the current character might start a nested comment.
            if next_char == '<':
                # Look ahead two characters to see if they form the start of a nested comment.
                if t.lexer.lexdata[t.lexer.lexpos:t.lexer.lexpos + 2] == '<%':
                    comment_depth += 1  # Increase depth for a new nested comment.
                    t.lexer.lexpos += 2  # Skip past the '<%' marker.
                else:
                    t.lexer.lexpos += 1  # Not a comment start, just move past '<'.

            # Check if the current character might end a comment.
            elif next_char == '%':
                # Look ahead two characters to check for comment end marker.
                if t.lexer.lexdata[t.lexer.lexpos:t.lexer.lexpos + 2] == '%>':
                    comment_depth -= 1  # Decrease depth as we close a comment.
                    t.lexer.lexpos += 2  # Skip past the '%>' marker.
                    if comment_depth == 0:
                        break  # Exit the loop if no more nested comments.
                else:
                    t.lexer.lexpos += 1  # Not a comment end, just move past '%'.

            # Handle all other characters.
            else:
                if next_char == '\n':
                    t.lexer.lineno += 1  # Update line number for new lines.
                t.lexer.lexpos += 1  # Move to the next character.

        # Set the value of the token to the entire comment text (optional if you're ignoring comments).
        t.value = t.lexer.lexdata[t.lexer.comment_start:t.lexer.lexpos]
        return None  # Return None to ignore the token, or return 't' if capturing comment content.

    def t_IDENTIFIER(self, t):
        # Matches identifiers and checks if they are keywords.
        #
        # Parameters:
        #     t (LexToken): The token object.
        #
        # Returns:
        #     LexToken: The token object with updated type if it's a keyword.

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
            'to': 'TO',
            'scan': 'SCAN',
            'print': 'PRINT',
            'list': 'LIST',
            'length': 'LENGTH',
            'exit': 'EXIT'
        }
        # Check if the identifier is a keyword, update token type accordingly
        t.type = keywords.get(t.value, 'IDENTIFIER')
        return t

    # This function is defined to handle errors that occur during tokenization.
    def t_error(self, t):
        """
        Handles errors during tokenization.

        Parameters:
            t (LexToken): The token object.
        """
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
