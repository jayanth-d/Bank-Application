class Account:
    def __init__(self,username, accno, password, balance):
        self.name = username
        self.accno = accno 
        self.password = password
        self.balance = balance
    
    def deposit(self, amount):
        bal = int(self.balance)
        bal += amount
        self.balance = str(bal)
    
    def withdraw(self, amount):
        bal = int(self.balance)
        if bal < amount:
            return 0
        else:
            bal -= amount
            self.balance = str(bal)
            return 1
    
    def transfer(self, amount, obj):
        bal = int(self.balance)
        if bal < amount:
            return 0
        else:
            bal -= amount
            bal2 = int(obj.balance)
            bal2 += amount
            obj.balance = str(bal2)
            self.balance = str(bal)
            return 1
        
    def balance(self):
        return self.balance
    