__name__ = 'SymbolTable'

HEAP = 1
STACK = -1

param_registers = ['%rdi', '%rsi', '%rdx', '%rcx', '%r8', '%r9', '%r10', '%r11', '%r12', '%r13', '%r14', '%r15']

class SymbolTable:
    def __init__(self):
        self.scope = []
        self.stack_pointer = []
        self.heap_pointer = 0

    def enterScope(self):
        self.scope.append([])
        self.stack_pointer.append(0)

    def exitScope(self):
        self.scope.pop()
        self.stack_pointer.pop()

    def addSymbol(self, symbol):
        if symbol.size:
            if symbol.mem == HEAP:
                self.heap_pointer += symbol.size
                symbol.pointer = self.heap_pointer
            else:
                self.stack_pointer[-1] += symbol.size
                symbol.pointer = self.stack_pointer[-1]
            
        self.scope[-1].append(symbol)

    def probe(self, id):
        local_scope = self.scope[-1]
        for symbol in local_scope:
            if symbol.id == id:
                return symbol
        return None

    def lookup(self, id):
        for i in range(len(self.scope)):
            local_scope = self.scope[-(i + 1)]
            for symbol in local_scope:
                if symbol.id == id:
                    return symbol
        return None

class VarSymbol:
    def __init__(self, id, type, line, size, mem):
        self.id = id
        self.type = type
        self.line = line
        self.size = size
        self.mem = mem
        self.pointer = 0
    
    def getAddr(self):
        return self.mem * self.pointer

class MethodSymbol:
    def __init__(self, id, type, line, params):
        self.id = id
        self.type = type
        self.line = line
        self.params = params
        self.size = 0