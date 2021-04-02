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
                print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                logged_option = input(">")
                if logged_option == "1":
                    print(f"\nBalance: {self.balance}")
                elif logged_option == "2":
                    pass
                    # Enter income:
                    # >10000
                    # Income was added!
                elif logged_option == "3":
                    pass
                    # Transfer
                    # Enter card number:
                    # >4000003305160035
                    # # Probably you made a mistake in the card number. Please try again!
                    # Such a card does not exist.
                    # Enter how much money you want to transfer:
                    # >15000
                    # Not enough money!
                    # Success!
                elif logged_option == "4":
                    pass
                elif logged_option == "5":
                    pass
                elif logged_option == "0":
                    print("\nBye!")
                    exit()
                else:
                    print("\nInvalid option")
        else:
            print("\nwrong")

# 1. Balance
# 2. Add income
# 3. Do transfer
# 4. Close account
# 5. Log out
# 0. Exit

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
