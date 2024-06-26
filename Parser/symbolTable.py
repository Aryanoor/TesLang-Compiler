class Symbol:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.used = False

    def mark_as_used(self):
        self.used = True

    def __str__(self):
        return f'<Symbol: {self.name}>'


class VariableSymbol(Symbol):
    def __init__(self, name, varType, assigned, pos):
        super().__init__(name, pos)
        self.type = varType
        self.assigned = assigned
        self.register = None

    def set_register(self, register):
        self.register = register


class VectorSymbol(Symbol):
    def __init__(self, name, length, pos):
        super().__init__(name, pos)
        self.length = length
        self.type = 'vector'


class FunctionSymbol(Symbol):
    def __init__(self, name, rettype, params, pos):
        super().__init__(name, pos)
        self.rettype = rettype
        self.params = params

    def __str__(self):
        return f'<Function: {self.name} returns {self.rettype} params({self.params})>'


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.table = {}

    def put(self, symbol):
        if symbol.name not in self.table:
            self.table[symbol.name] = symbol
            return True
        return False

    def get(self, name, current_scope_only=False):
        if name in self.table:
            return self.table[name]
        if not current_scope_only and self.parent:
            return self.parent.get(name)
        return None

    def mark_as_used(self, name):
        symbol = self.get(name)
        if symbol:
            symbol.mark_as_used()

    def print_symbols(self):
        for name, symbol in self.table.items():
            print(f'{name}: {symbol}')

    def show_unused_warnings(self):
        for symbol in self.table.values():
            if not symbol.used:
                print(f'Warning: Unused {symbol.__class__.__name__} "{symbol.name}" at line {symbol.pos}')

