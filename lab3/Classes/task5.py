class Bank_acc:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    def deposit(self,to_deposit):
        self.balance += to_deposit
        print("Your balance was updated: ", self.balance)
    def withdrawal(self, money):
        if money > self.balance:
            print("Error")
        else:
            self.balance -= money
            print("Success")

p1 = Bank_acc("b", 100)
p1.withdrawal(99)
print(p1.balance)
p1.withdrawal(2)
p1.deposit(1)
print(p1.balance)
p1.withdrawal(1)
print(p1.balance)

        