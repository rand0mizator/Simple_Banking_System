import random
from string import digits

accounts = []  # all account in object type
current_account = None  # when logged its related to object from accounts
exit_flag = False   


class Account:
    def __init__(self):
        self.card_number = '400000' + ''.join(random.choice(digits) for x in range(10))  # construct card number in form of
                                                                                         # 400000DDDDDDDDDD
        self.pin = ''.join(random.choice(digits) for x in range(4))  # construct pin in form of DDDD
        self.balance = 0


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
            
            
