from Parser.symbolTable import *
from Parser.AST import *


class SemanticChecker:
    def __init__(self):
        self.current_table = SymbolTable(parent=None)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_FunctionDefinition(self, node):
        func_symbol = FunctionSymbol(node.name, node.return_type, node.params, node.pos)
        if not self.current_table.put(func_symbol):
            print(f"Semantic Error: Function '{node.name}' is already defined.")
        else:
            # Create a new scope for the function
            old_table = self.current_table
            self.current_table = SymbolTable(parent=old_table)
            # Visit function parameters and body
            for param in node.params:
                self.visit(param)
            self.visit(node.body)
            # Restore the old table
            self.current_table = old_table
            self.current_table.show_unused_warnings()

    def visit_Parameter(self, node):
        param_symbol = VariableSymbol(node.name, node.type, True, node.pos)
        if not self.current_table.put(param_symbol):
            print(f"Semantic Error: Parameter '{node.name}' is already defined in this scope.")

    def visit_VariableDeclaration(self, node):
        var_symbol = VariableSymbol(node.identifier, node.type, node.initializer is not None, node.pos)
        if not self.current_table.put(var_symbol):
            print(f"Semantic Error: Variable '{node.identifier}' is already defined.")

    def visit_Body(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_BinaryOp(self, node):
        # Perform type checking and visit child nodes
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.operand)

    def visit_Return(self, node):
        self.visit(node.expr)

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileLoop(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_ForLoop(self, node):
        self.visit(node.variable)
        self.visit(node.start_expr)
        self.visit(node.end_expr)
        self.visit(node.body)
