from Parser.symbolTable import SymbolTable, FunctionSymbol, VariableSymbol
from Parser.AST import *


class PreParser:
    def __init__(self):
        self.global_symbol_table = SymbolTable(parent=None)
        self.setup_builtins()

    def setup_builtins(self):
        # Add built-in functions to the global symbol table
        builtins = [
            FunctionSymbol('print', 'null', [Parameter('string_to_print', 'str', None)], None),
            FunctionSymbol('printInt', 'null', [Parameter('int_to_print', 'int', None)], None),
            FunctionSymbol('length', 'int', [Parameter('vector_to_count', 'vector', None)], None),
            FunctionSymbol('scan', 'int', [], None),
            FunctionSymbol('list', 'vector', [Parameter('size', 'int', None)], None)
        ]

        for builtin in builtins:
            self.global_symbol_table.put(builtin)

    def visit(self, node):
        """ General visit method that delegates to node-specific methods """
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, self.global_symbol_table)

    def generic_visit(self, node, table):
        """ Called if no explicit visitor function exists for a node """
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node, table):
        for child in node.children:
            self.visit(child, table)

    def visit_FunctionDefinition(self, node, table):
        func_symbol = FunctionSymbol(node.name, node.return_type, node.params, node.pos)
        if not table.put(func_symbol):
            print(f"Error: Function '{node.name}' is already defined at line {node.pos}.")
        else:
            new_scope_table = SymbolTable(parent=table)
            for param in node.params:
                param_symbol = VariableSymbol(param.name, param.type, True, param.pos)
                if not new_scope_table.put(param_symbol):
                    print(f"Error: Parameter '{param.name}' is already defined at line {param.pos}.")
            if node.body:
                self.visit(node.body, new_scope_table)

    def visit_Body(self, node, table):
        for stmt in node.statements:
            self.visit(stmt, table)

    def visit_VariableDeclaration(self, node, table):
        var_symbol = VariableSymbol(node.identifier, node.type, node.initializer is not None, node.pos)
        if not table.put(var_symbol):
            print(f"Semantic Error: Variable '{node.identifier}' already defined at line {node.pos}.")

    # Implement other node visitors based on the node types in your AST
