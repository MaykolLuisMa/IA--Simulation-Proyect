class CompanyRegister:
    def __init__(self):
        self.actions = []
        self.value = []
    def __len__(self):
        return len(self.actions)
class Register:
    def __init__(self, companies):
        self.companies_registers = {corp.id:CompanyRegister() for corp in companies}
        self.inflation = []