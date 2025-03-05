import re
class Format():
    def check_the_format_of_n_id (n_id: str) -> str:
        correct_n_id = False
        while correct_n_id == False:
            check_n_id = re.match(r"^\d{10}$", n_id)
            if check_n_id != None:
                correct_n_id = True
                return n_id
            else:
                n_id = input ("Invalid National id\nPlease Enter it again: ")

    def check_the_format_of_phone_number (tel: str) -> str:
        correct_tel = False
        while correct_tel == False:
            check_tel = re.match(r"^09\d{9}$", tel)
            if check_tel != None:
                correct_tel = True
                return tel
            else:
                tel = input ("Invalid Phone number\nPlease Enter it again: ")

    def check_the_format_of_username (username: str) -> str:
        correct_username = False
        while correct_username == False:
            check_username = re.match(r"^[A-z]\S{7,20}$", username)
            if check_username != None:
                correct_username = True
                return username
            else:
                username = input("Invalid Username\nPlease Make another one: ")

    def check_the_format_of_password (password: str) -> str:
        correct_password = False
        while correct_password == False:
            check_password = re.match(r"(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password)
            if check_password != None:
                correct_password = True
                return password
            else:
                password = input ("Not a Strong Password (Use @.,#!?)\nPlease Enter a strong one: ")