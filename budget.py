class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def item_line(self, item):
        return item.get('description')[0:23] + ''.join([' ' for _ in range(30 - min(23, len(item.get('description'))) - len(format(item.get('amount'), '.2f')))]) + format(item.get('amount'), '.2f') + '\n'

    def __str__(self):
        str = self.name.center(30).replace(' ','*') + '\n'
        for item in self.ledger:
            str += self.item_line(item) 
        str += f'Total: {self.get_balance()}'
        return str

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if (self.check_funds(amount)):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        return sum(map(lambda obj : obj.get('amount'), self.ledger))

    def transfer(self, amount, category):
        if (self.check_funds(amount)):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False
        
    def check_funds(self, amount):
        return not amount > self.get_balance()

    def get_money_spent(self):
        withdraws = filter(lambda val: val < 0, map(lambda obj: obj.get('amount'), self.ledger))
        return -sum(withdraws)

def create_spend_chart(categories):
    s = 'Percentage spent by category\n'
    total_money_spent = sum(map(lambda category: Category.get_money_spent(category), categories))
    percentages = dict()
    for category in categories:
        percentages.update({category.name: (Category.get_money_spent(category) / total_money_spent) * 100})

    print(percentages)

    rounded_percentages = list(map(lambda percentage: round(percentage / 10) * 10, list(percentages.values())))

    for n in range(100, -1, -10):
        s += f"{str(n)+'|':>4}"
        for percentage in rounded_percentages:
            if percentage >= n:
                s += ' o '
            else:
                s += '   '

        s += '\n'

    s += '    ' + ''.join(['-' for _ in range(len(rounded_percentages) * 3 + 1)]) + '\n'

    longest_category_name_length = max(list(map(lambda category: len(category.name), categories)))

    category_name_lengths = dict()
    for category in categories:
        category_name_lengths.update({category.name: len(category.name)})

    for i in range(longest_category_name_length):
        s += '   '

        for category in categories:
            if (category_name_lengths[category.name] > i):
                s += '  ' + category.name[i]
            else:
                s += '   '
        s += '\n'

    return s

food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
actual = create_spend_chart([business, food, entertainment])
expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "

print(expected) 
print(actual)







