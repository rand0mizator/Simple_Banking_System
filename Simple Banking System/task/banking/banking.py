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
                    number TEXT,
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

    def add_income(self):
        print("Enter income:")
        income = int(input(">"))
        self.balance += income
        print("Income was added!")
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        balance_card_number = (self.balance, self.card_number)
        cur.execute("""UPDATE card SET balance = ? WHERE number = ?""", balance_card_number)
        conn.commit()
        conn.close()

    def transfer_money(self, card_number, money):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""SELECT number, balance FROM card WHERE number = ?""", (card_number,))
        row = cur.fetchone()
        target_balance = int(row[1] + money)
        combo1 = (target_balance, card_number)
        cur.execute("""UPDATE card SET balance = ? WHERE number = ?""", combo1)
        self.balance -= money
        combo2 = (self.balance, self.card_number)
        cur.execute("""UPDATE card SET balance = ? WHERE number = ?""", combo2)
        conn.commit()
        conn.close()

    @staticmethod
    def validate_checksum(card_number):
        sum1 = 0
        check_digit = '0'
        for digit in enumerate(card_number[:-1], 1):
            n = 0
            if digit[0] % 2:
                n = int(digit[1]) * 2
                if n > 9:
                    n = n - 9
            else:
                n = int(digit[1])
            sum1 += n
        if not sum1 % 10:
            check_digit = '0'
        else:
            check_digit = str(10 - sum1 % 10)
        if check_digit == card_number[-1]:
            return True
        return False

    @staticmethod
    def is_card_exist(card_number):
        # check whether card is present in database
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""SELECT number FROM card WHERE number = ?""", (card_number,))
        if cur.fetchone():
            conn.commit()
            conn.close()
            return True
        conn.commit()
        conn.close()
        return False

    def close_account(self):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("""DELETE FROM card WHERE number = ?""", (self.card_number,))
        conn.commit()
        conn.close()

    def log_into_account(self, card_number, card_pin):
        if self.verify_credentials(card_number, card_pin):
            self.card_number = card_number
            self.card_pin = card_pin
            print("\nYou have successfully logged in!")
            while True:
                print("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                logged_option = input(">")
                if logged_option == "1":
                    print(f"\nBalance: {self.balance}")
                elif logged_option == "2":
                    # add income
                    self.add_income()
                elif logged_option == "3":
                    print("Transfer")
                    print("Enter card number:")
                    destination_card = input(">")
                    if destination_card[0] != '4':
                        print("Such a card does not exist.")
                    elif not self.validate_checksum(destination_card):
                        print("Probably you made a mistake in the card number. Please try again!")
                    # elif not self.is_card_exist(destination_card):
                    #     print("Such a card does not exist.")
                    elif destination_card == self.card_number:
                        print("You can't transfer money to the same account!")
                    else:
                        print("Enter how much money you want to transfer:")
                        money = int(input(">"))
                        if self.balance - money >= 0:
                            self.transfer_money(destination_card, money)
                        else:
                            print("Not enough money!")
                elif logged_option == "4":
                    self.close_account()
                elif logged_option == "5":
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
        for fetch in cur.fetchall():
            print(fetch)
        conn.close()


while True:
    CreditCard.create_table()
    card = CreditCard()
    print("\n1. Create an account\n2. Log into account\n0. Exit")
    option = input(">")
    if option == "1":
        card.create_account()
    elif option == "2":
        print("Enter your card number:")
        card_number_input = input(">")
        print("Enter your PIN:")
        card_pin_input = input(">")
        card.log_into_account(card_number_input, card_pin_input)
    elif option == "3":
        card.print_table()

    elif option == "0":
        print("\nBye!")
        exit()
    else:
        print("\nIncorrect option")
