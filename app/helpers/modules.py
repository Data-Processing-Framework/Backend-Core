list_of_modules = []


class n_module:
    def _init_(self, name, id, type, module):
        self.name = name
        self.id = id
        self.type = type
        self.module = module

    def getList(self):
        return list_of_modules

    def createModule(self, name, id, type, module):
        module = n_module(name, id, type, module)
        self.addToList(module)
        return module

    def addToList(self, n_module):
        if n_module not in list_of_modules:
            list_of_modules.append(n_module)

    def removeFromList(self, n_module):
        list_of_modules.remove(n_module)
