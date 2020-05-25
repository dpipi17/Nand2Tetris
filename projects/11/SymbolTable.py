
class SymbolTable:

    indexes = {
        'static' : 0, 
        'this' : 0, 
        'local' : 0, 
        'argument' : 0
    }

    static_kind_table = {}

    def __init__(self):
        self.class_type_table = {}
        self.subroutine_type_table = {}
        self.indexes['this'] = 0
        self.indexes['local'] = 0
        self.indexes['argument'] = 0

    def start_subroutine(self):
        self.subroutine_type_table = {}
        self.indexes['local'] = 0
        self.indexes['argument'] = 0

    def define(self, name, type, kind):
        defined_tuple = (type, kind, self.__next_index(kind))

        if kind == 'this':
            self.class_type_table[name] = defined_tuple
        elif kind in ['local', 'argument']:
            self.subroutine_type_table[name] = defined_tuple
        else:
            self.static_kind_table[name] = defined_tuple

    def var_count(self, kind):
        return self.indexes[kind]

    def kind_of(self, name):
        if name in self.subroutine_type_table:
            return self.subroutine_type_table[name][1]
        elif name in self.class_type_table:
            return self.class_type_table[name][1]
        elif name in self.static_kind_table:
            return self.static_kind_table[name][1]

        return None

    def type_of(self, name):
        if name in self.subroutine_type_table:
            return self.subroutine_type_table[name][0]
        elif name in self.class_type_table:
            return self.class_type_table[name][0]
        elif name in self.static_kind_table:
            return self.static_kind_table[name][0]

        return None

    def index_of(self, name):
        if name in self.subroutine_type_table:
            return self.subroutine_type_table[name][2]
        elif name in self.class_type_table:
            return self.class_type_table[name][2]

        return self.static_kind_table[name][2]

    def __next_index(self, kind):
        index = self.indexes[kind]
        self.indexes[kind] = index + 1
        return index
        
