class Node:
    """Base class for all AST nodes."""
    def __init__(self, pos):
        self.pos = pos

    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__
        visitor = getattr(visitor, method_name, self.generic_visit)
        return visitor(self)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(self.__class__.__name__))


class Program(Node):
    """Represents the root of the program."""
    def __init__(self, children, pos):
        super().__init__(pos)
        self.children = children


class FunctionDefinition(Node):
    """Node for function definitions."""
    def __init__(self, name, params, return_type, body, pos):
        super().__init__(pos)
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body


class Return(Node):
    """Node for return statements."""
    def __init__(self, expr, pos):
        super().__init__(pos)
        self.expr = expr



class BinaryOp(Node):
    """Node for binary operations."""
    def __init__(self, left, operator, right, pos):
        super().__init__(pos)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(Node):
    """Node for unary operations."""
    def __init__(self, operator, operand, pos):
        super().__init__(pos)
        self.operator = operator
        self.operand = operand


class VariableDeclaration(Node):
    """Node for variable declarations."""
    def __init__(self, identifier, type_, initializer, pos):
        super().__init__(pos)
        self.identifier = identifier
        self.type = type_
        self.initializer = initializer


class IfStatement(Node):
    """Node for if statements."""
    def __init__(self, condition, then_branch, else_branch, pos):
        super().__init__(pos)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileLoop(Node):
    """Node for while loops."""
    def __init__(self, condition, body, pos):
        super().__init__(pos)
        self.condition = condition
        self.body = body


class ForLoop(Node):
    """Node for for loops."""
    def __init__(self, variable, start_expr, end_expr, body, pos):
        super().__init__(pos)
        self.variable = variable
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body


class Body(Node):
    """Node representing a sequence of statements (could be used for blocks)."""
    def __init__(self, statements, pos):
        super().__init__(pos)
        self.statements = statements


class Parameter(Node):
    """
    Node for function parameters.
    """
    def __init__(self, name, type_, pos):
        super().__init__(pos)
        self.name = name
        self.type = type_

    def __repr__(self):
        return f"Parameter(name={self.name}, type={self.type}, pos={self.pos})"


class Expression(Node):
    """Base class for all expressions."""
    def __init__(self, pos):
        super().__init__(pos)


class Identifier(Expression):
    """Node for identifiers."""
    def __init__(self, name, pos):
        super().__init__(pos)
        self.name = name


class Number(Expression):
    """Node for numeric literals."""
    def __init__(self, value, pos):
        super().__init__(pos)
        self.value = value

# Add more node types as required by your parser.