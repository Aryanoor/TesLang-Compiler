class NodeVisitor:
    def visit(self, node):
        """Visit a node."""
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_FunctionDefinition(self, node):
        print(f"Visiting Function Definition: {node.name}")
        for param in node.params:
            self.visit(param)
        self.visit(node.body)

    def visit_Return(self, node):
        print("Visiting Return Node")
        self.visit(node.expr)

    def visit_BinaryOp(self, node):
        print(f"Visiting Binary Operation: {node.operator}")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        print(f"Visiting Unary Operation: {node.operator}")
        self.visit(node.operand)

    def visit_VariableDeclaration(self, node):
        print(f"Declaring Variable: {node.identifier} of Type: {node.type}")
        if node.initializer:
            self.visit(node.initializer)

    def visit_IfStatement(self, node):
        print("Visiting If Statement")
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileLoop(self, node):
        print("Visiting While Loop")
        self.visit(node.condition)
        self.visit(node.body)

    def visit_ForLoop(self, node):
        print("Visiting For Loop")
        self.visit(node.variable)
        self.visit(node.start_expr)
        self.visit(node.end_expr)
        self.visit(node.body)

    def visit_Body(self, node):
        print("Visiting Body")
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Parameter(self, node):
        print(f"Parameter: {node.name}, Type: {node.type}")

    def visit_Identifier(self, node):
        print(f"Identifier: {node.name}")

    def visit_Number(self, node):
        print(f"Number: {node.value}")