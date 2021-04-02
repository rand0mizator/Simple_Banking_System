import random
import sqlite3


class CreditCard:
    IIN = "400000"

    def __init__(self):
        self.checksum = 0
        self.card_number = None
        self.card_pin = None
        self.balance = 0

    @staticmethod
    def create_table():
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS card(
                    id INTEGER PRIMARY KEY, 
                    'number' TEXT,
                    pin TEXT,
                    balance INTEGER DEFAULT(0))""")
        conn.commit()
        conn.close()

    @staticmethod
    def add_account_to_db(card_nr, pin):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""INSERT INTO card 
                            ('number', 'pin') VALUES (?, ?)
                            """, (card_nr, pin))
        conn.commit()
        conn.close()

    def generate_card_number(self):
        self.card_number = list(CreditCard.IIN) + [str(random.randint(0, 9)) for _ in range(9)]
        int_card_number = list(map(int, self.card_number))
        for digit in range(len(int_card_number)):
            if digit % 2 == 0:
                int_card_number[digit] *= 2
                if int_card_number[digit] > 9:
                    int_card_number[digit] -= 9
        total_digits = sum(int_card_number)
        while total_digits % 10 != 0:
            total_digits += 1
            self.checksum += 1
        self.card_number.append(str(self.checksum))
        self.card_number = "".join(self.card_number)

    def create_account(self):
        self.generate_card_number()
        self.card_number = f"{self.card_number}"
        self.card_pin = "".join([str(random.randint(0, 9)) for _ in range(4)])
        print("Your card has been created")
        print(f"Your card number:")
        print(self.card_number)
        print(f"Your card PIN:")
        print(f"{self.card_pin}")
        self.add_account_to_db(self.card_number, self.card_pin)

    @staticmethod
    def verify_credentials(card_number, card_pin):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT number, pin FROM card")
        accounts = cur.fetchall()
        conn.commit()
        for acc_info in accounts:
            if card_number in acc_info and card_pin in acc_info:
                conn.close()
                return True
        conn.close()
        return False

    def log_into_account(self, card_number, card_pin):
        if self.verify_credentials(card_number, card_pin):
            print("\nYou have successfully logged in!")
            while True:
                print("\n1. Balance\n2. Log out\n0. Exit")
                logged_option = input(">")
                if logged_option == "1":
                    print(f"\nBalance: {self.balance}")
                elif logged_option == "2":
                    print("\nYou have successfully logged out!")
                    break
                elif logged_option == "0":
                    print("\nBye!")
                    exit()
                else:
                    print("\nInvalid option")
        else:
            print("\nwrong")

    @staticmethod
    def print_table():
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM card")
        conn.commit()
        print(cur.fetchall())


while True:
    CreditCard.create_table()
    card = CreditCard()
    print("\n1. Create an account\n2. Log into account\n0. Exit")
    option = input(">")
    if option == "1":
        card.create_account()
    elif option == "2":
        card_number_input = input("\nEnter your card number:\n")
        card_pin_input = input("Enter your PIN:\n")
        card.log_into_account(card_number_input, card_pin_input)
    elif option == "3":
        card.print_table()

    elif option == "0":
        print("\nBye!")
        exit()
    else:
        print("\nIncorrect option")
"""Structure
class Account:

@staticmethod
def create_table()

@staticmethod
def add_account_to_db(card_nr, pin)

def generate_card_number(self)

def create_account(self):

@staticmethod
def verify_credentials(card_number, card_pin)

def log_into_account(self, card_number, card_pin):
"""


import random
import sqlite3


ISSUER_IDENTIFICATION_NUMBER = '400000'  # constant for this stage of project

accounts = []  # all accounts in object type
current_account = None  # when logged its related to object from accounts
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class Account:
    def __init__(self):
        self.card_number = generate_card_number()
        self.pin = ''.join(random.choice(digits) for x in range(4))  # construct pin in form of DDDD
        self.balance = 0


def quit():
    print("Bye!")
    conn.commit()
    conn.close()
    exit()  # built in function in python, very nice isnt it?


def generate_check_digit(ISSUER_IDENTIFICATION_NUMBER, customer_account_number):
    """ Luhn algo Implementation for 16th digit """
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
    """"Generates card number as IIN + customer account number + check digit (through Luhn algo), checks uniqueness"""
    global accounts
    customer_account_number = ''.join(random.choice(digits) for x in range(9))
    check_digit = generate_check_digit(ISSUER_IDENTIFICATION_NUMBER, customer_account_number)
    card_number = ISSUER_IDENTIFICATION_NUMBER + customer_account_number + check_digit
    for account in accounts:
        # TODO dunno will it work properly in production
        if card_number == account.card_number:  # if generated card number already in accounts
            card_number = generate_card_number()  # generate it again o_O
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
    """ prints all card numbers and pins in [accounts] for debug purposes """
    for account in accounts:
        print(account.card_number, account.pin)


def store_to_db(accounts):
    for account in accounts:
        cur.execute('INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)',
                    (account.card_number, account.pin, account.balance))


if cur.fetchone():
    cur.execute('''CREATE TABLE card (id INTEGER,
                                 number TEXT,
                                 pin TEXT,
                                 balance INTEGER DEFAULT 0
                                 )''')
while True:
    print("""
        1. Create an account
        2. Log into account
        0. Exit
          """)
    input_ = input(">")

    if input_ == '1':
        create_account()
    elif input_ == '2':
        card_number = input("Enter your card number: > ")
        pin = input("Enter your PIN: > ")
        access_account(card_number, pin)
    elif input_ == '3':
        print_accounts_info()
    elif input_ == '0':
        quit()
    while current_account:  # if successfully logged in (current_account != None)
        print("""
        1. Balance
        2. Log out
        0. Exit
          """)
        input_ = input(">")
        if input_ == '1':
            check_balance()
        elif input_ == '2':
            logout()
        elif input_ == '0':
            quit()
    store_to_db(accounts)
    conn.commit()
