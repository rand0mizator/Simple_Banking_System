import random
from string import digits

ISSUER_IDENTIFICATION_NUMBER = '400000'

accounts = []  # all account in object type
current_account = None  # when logged its related to object from accounts
exit_flag = False


class Account:
    def __init__(self):
        self.card_number = generate_card_number()
        self.pin = ''.join(random.choice(digits) for x in range(4))  # construct pin in form of DDDD
        self.balance = 0


def generate_check_digit(ISSUER_IDENTIFICATION_NUMBER, customer_account_number):
    """Luhn algo Implementation"""
    sum1 = 0
    number = ISSUER_IDENTIFICATION_NUMBER + customer_account_number
    for digit in enumerate(number, 1):
        n = 0
        if digit[0] % 2:
            n = int(digit[1]) * 2
            if n > 9:
                n = n - 9
        else:
            n = int(digit[1])
        sum1 += n
    if not sum1 % 10:
        return '0'
    else:
        return str(10 - sum1 % 10)


def generate_card_number():
    """"Generates card number as IIN + customer account number + check digit (through Luhn algo)"""
    global accounts
    customer_account_number = ''.join(random.choice(digits) for x in range(9))
    check_digit = generate_check_digit(ISSUER_IDENTIFICATION_NUMBER, customer_account_number)
    card_number = ISSUER_IDENTIFICATION_NUMBER + customer_account_number + check_digit
    for account in accounts:
        if card_number == account.card_number:
            card_number = generate_card_number()
    return card_number


def create_account():
    """creates objects of Account class, adds to 'Database' and prints card number and pin"""
    global accounts  # to allow changing global variable inside function
    account = Account()  # create object of Account class
    accounts.append(account)  # add object of Account class to "Database"
    print("Your card has been created")
    print("Your card number:")
    print(account.card_number)
    print("Your card PIN:")
    print(account.pin)


def access_account(card_number, pin):
    """grants access to account via card number and pin, changes global variable 'current_account' """
    global current_account
    for account in accounts:
        if account.card_number == card_number and account.pin == pin:
            current_account = account
            return print("You have successfully logged in!")
            
    else:
        print("Wrong card number or PIN!")

def logout():
    """changes global variable 'current_account' """
    global current_account
    current_account = None
    print("You have successfully logged out!")


def check_balance():
    """if successfully logged into account (aka current_account != None) prints out its balance"""
    print(f"Balance: {current_account.balance}")


def print_accounts_info():
    for account in accounts:
        print(account.card_number, account.pin)
    


while True:
    if exit_flag:
        print("Bye!")
        break
        
    print("""
        1. Create an account
        2. Log into account
        0. Exit
          """)
    input_ = input()
    
    if input_ == '1':
        create_account()

    elif input_ == '2':
        cn = input("card number")
        p = input("pin")
        access_account(cn, p)
               
    elif input_ == '3':
        print_accounts_info()

    elif input_ == '0':
        exit_flag = True

    while current_account:  # if successfully logged in (current_account != None) 
        print("""
        1. Balance
        2. Log out
        0. Exit
          """)
        input_ = input()
        if input_ == '1':
            check_balance()
        elif input_ == '2':
            logout()
        elif input_ == '0':
            exit_flag = True
            break
            
            