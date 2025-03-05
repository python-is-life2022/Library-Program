import re
from datetime import datetime
from check_formats import Format
from mysql.connector import Connect, IntegrityError, DataError
cnx = Connect (username = '',
               password = '',
               host = 'localhost',
               database = 'library')
print ("Connected successfully")
query = cnx.cursor()
format = Format()
class Users():
    def __init__ (self, f_name, l_name, age, b_date, tel, n_id, username, password):
        self.first_name = f_name
        self.last_name = l_name
        self.age = age
        self.birthdate = b_date
        self.phone_number = tel
        self.national_id = n_id
        self.username = username
        self.password = password

    def create_an_account (self):
        check_n_id, check_tel, check_username = False, False, False
        while check_n_id == False and check_tel == False and check_username == False:
            try:
                query.execute ("INSERT INTO users (f_name, l_name, age, b_date, tel, n_id, username, pass_w)"\
                            "VALUES (\'%s\', \'%s\', \'%i\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (self.first_name,
                                                                                                         self.last_name,
                                                                                                         self.age,
                                                                                                         self.birthdate,
                                                                                                         self.phone_number,
                                                                                                         self.national_id,
                                                                                                         self.username,
                                                                                                         self.password))
            except IntegrityError:
                query.execute ("SELECT tel, n_id, username FROM users")
                unique_data = query.fetchall()
                i = 0
                duplicate_tel, duplicate_n_id, duplicate_username = True, True, True
                while duplicate_tel == True and duplicate_n_id == True and duplicate_username == True:
                    if self.phone_number in unique_data[i]:
                        self.phone_number = format.check_the_format_of_phone_number(input("One User had same phone number with you\nEnter it again: "))
                        duplicate_tel = False
                    if self.national_id in unique_data[i]:
                        self.national_id = format.check_the_format_of_n_id(input("One User found with this national id\nEnter it again: "))
                        duplicate_n_id = False
                    if self.username in unique_data[i]:
                        self.username = format.check_the_format_of_username(input("One User found with this username\nMake another one: "))
                        duplicate_username = False
                    i += 1
            except DataError:
                print ("You Entered Wrong data!")
            except:
                print ("Exception Rised!")
            else:
                print ("One User add!")
                cnx.commit()
                check_n_id, check_tel, check_username = True, True, True

class Books ():
    def __init__ (self, name, writer, genre, pages, prints):
        self.book_name = name
        self.writer = writer 
        self.genre = genre
        self.pages_count = pages
        self.prints_count = prints

    def add_book_in_database (self):
        query.execute ("INSERT INTO books (book_name, writer, genre, print_count, pages_count)"\
                       "VALUES (\'%s\', \'%s\', \'%s\', \'%i\', \'%i\')" % (self.book_name,
                                                                            self.writer,
                                                                            self.genre,
                                                                            self.prints_count,
                                                                            self.pages_count))
        cnx.commit()
        print ("One Book add!")

main_parts = int(input("\nWelcome to our library\n1)Users\n2)Books\nWhich part of this app: "))
match main_parts:
    case 1:
        print ("\n          * * Users part * *          ")
        user_parts = int(input("1)Sign Up\n2)Logging\nWhich part of the users: "))
        match user_parts:
            case 1:
                print ("\n          * * Create an account * *          ")
                f_name = input ("Please enter your Firstname: ").title()
                l_name = input ("Please enter your Lastname: ").title()
                correct_date = False
                while correct_date == False:
                    b_date = input("Please enter your Birthdate: ")
                    birth_date_parts = re.split(r"[/,:\-]", b_date)
                    b_year = int(birth_date_parts[0])
                    b_month = int(birth_date_parts[1])           
                    b_day = int(birth_date_parts[2])
                    if b_month >= 1 and b_month <= 12 and b_day >= 1 and b_day <= 31:
                        correct_date = True
                        today_year = datetime.now().year
                        today_month = datetime.now().month
                        today_day = datetime.now().day
                        if today_month < b_month:
                            age = (today_year - b_year) - 1
                        elif today_month == b_month:
                            if today_day < b_day:
                                age = (today_year - b_year) - 1
                            else:
                                age = today_year - b_year
                        else:
                            age = today_year - b_year
                    else:
                        print ("Invalid date")
                tel = format.check_the_format_of_phone_number (input("Please enter your Phone number: "))
                n_id = format.check_the_format_of_n_id (input ("Please enter your National id: "))
                username = format.check_the_format_of_username (input ("Please make your Username: "))
                password = format.check_the_format_of_password (input  ("Please make your password: "))
                user = Users (f_name, l_name, age, b_date, tel, n_id, username, password)
                user.create_an_account()
            case 2:
                print ("\n          * * Logging page * *          ")
                username = input("Please enter your username: ")
                password = input ("Please enter your password: ") 
                check_username, check_password = False, False
                while check_username == False and check_password == False:
                    try:
                        query.execute("SELECT id, f_name, l_name, age, b_date, n_id, tel, book_count FROM users WHERE username = \'%s\' AND pass_w = \'%s\'" % (username,
                                                                                                                                                            password))                           
                        user_data = query.fetchone()
                        user_book_count = user_data[7]
                        print (f"\nWelcome back {user_data[1]} {user_data[2]}\nYour Personal informations:\nID: {user_data[0]}\nAge: {user_data[3]}"\
                               f"\nBirthDate: {user_data[4]}\nNational id: {user_data[5]}\nPhone number: {user_data[6]}\n"\
                               f"You Borrowed {user_book_count} Books from our librarys.")
                        if user_book_count >= 0 and user_book_count < 2:
                            print (f"\nYou can borrow {2 - user_book_count} Books from our library.\n")
                            query.execute("SELECT book_id, book_name, writer, genre, pages_count, book_count FROM books")
                            books_data = query.fetchall()
                            print("Books list:")
                            for book in books_data:
                                print (f"ID: {book[0]}, Name: {book[1]}, Writer: {book[2]}, Genre: {book[3]}, Pages count: {book[4]}, Count: {book[5]}")
                            book_id = int(input("Enter id of the book that you want: "))
                            query.execute("SELECT book_count FROM books WHERE book_id = \'%i\'" % book_id)
                            book_count = query.fetchone()[0]
                            if book_count > 0 and book_count <= 3:
                                query.execute("INSERT INTO borrow (user_id, book_id) VALUES (\'%i\', \'%i\')" % (user_data[0], book_id)) 
                                cnx.commit()                                                                              
                                book_count -= 1
                                user_book_count += 1
                                query.execute ("UPDATE users SET book_count = \'%i\' WHERE id = \'%i\'" % (user_book_count, user_data[0]))                                                                           
                                cnx.commit()                                                                              
                                query.execute ("UPDATE books SET book_count = \'%i\' WHERE book_id = \'%i\'" % (book_count, book_id))                                                                         
                                cnx.commit()                                                                              
                                print ("\nThanks You borrow one book right now")
                            elif book_count == 0:
                                print ("We don't have this book right now!")
                        elif user_book_count == 2:
                            print(f"\nPlease Return at least one of them.\n")
                            return_choose = int(input("Do you want return a book\n1)Yes 2)No:"))
                            match return_choose:
                                case 1:
                                    print (f"\nDear {user_data[1]} {user_data[2]}, Your books list: ")
                                    query.execute("SELECT br.user_id, br.book_id, b.book_name, b.writer, b.genre, b.book_count FROM borrow br JOIN books b ON br.book_id = b.book_id AND br.user_id = \'%i\'" % user_data[0])
                                    user_borrows = query.fetchall()
                                    i = 1
                                    for user in user_borrows:
                                        print (f"{i}) ID: {user[1]}, Name: {user[2]}, Writer: {user[3]}, Genre: {user[4]}")
                                        i += 1
                                    book_id = int(input("\nEnter the id of a book that you want to return: "))
                                    query.execute("SELECT book_count FROM books WHERE book_id = \'%i\'" % book_id)
                                    book_count = query.fetchone()[0]
                                    query.execute("DELETE FROM borrow WHERE user_id = \'%i\' AND book_id = \'%i\'" % (user_data[0], book_id))
                                    cnx.commit()
                                    book_count += 1 # Book count changes
                                    query.execute("UPDATE books SET book_count = \'%i\' WHERE book_id = \'%i\'" % (book_count, book_id))
                                    cnx.commit()
                                    user_book_count -= 1 # User book count chages
                                    query.execute ("UPDATE users SET book_count = \'%i\' WHERE id = \'%i\'" % (user_book_count, user_data[0]))
                                    cnx.commit()
                                    print ("Book Returned Succesfully")
                                case 2:
                                    print ("\nIt's ok, But you can't borrow any books until you return at least one of them.")
                                case _:
                                    print ("Invalid Number!")
                        check_username = True
                        check_password = True
                    except Exception:
                        query.execute ("SELECT username, pass_w FROM users")
                        usernames_and_passwords = query.fetchall()
                        i = 0
                        correct_username, correct_password = False, False
                        while i < len(usernames_and_passwords) and correct_username == False and correct_password == False:
                            if username in usernames_and_passwords[i]:
                                correct_username = True
                                if password in usernames_and_passwords[i]:
                                    correct_password = True
                                else:
                                    wrong_password_part = input("Incorrect password!\nDo you want to change your password if you forgot it(Yes/No): ")
                                    if wrong_password_part == 'Yes':
                                        password = format.check_the_format_of_password(input("Enter your new password: "))
                                        query.execute('UPDATE users SET pass_w = \'%s\' WHERE username = \'%s\'' % (password, username))
                                        cnx.commit()
                                        print("\nYour password changed successfully")
                                        correct_password = True
                                    elif wrong_password_part == 'No':
                                        password = input("Please enter your password again: ")
                                    else:
                                        print("Invalid input!")
                            i += 1
                        if correct_username == False:
                            check_username = True
                            print ("User not found!")
            case _:
                print ("Not Found!")
    case 2:
        print ("\n          * * Books part * *          ")
        book_name = input ("Book name: ").title()
        writer = input ("Writer name: ").title()
        g = int(input("1)Horror\n2)Romance\n3)History\n4)Crime\n5)Science fiction\n6)Action & Adventure\n7)Biography\n8)Mystery\n9)Fantasy\n10)Fiction\nWhat is the genre of book: "))
        match g:
            case 1:
                genre = "Horror"
            case 2:
                genre = "Romance"
            case 3:
                genre = "History"
            case 4:
                genre = "Crime"
            case 5:
                genre = "Science Fiction"
            case 6:
                genre = "Action & Adventure"
            case 7:
                genre = "Biography"
            case 8:
                genre = "Mystery"
            case 9:
                genre = "Fantasy"
            case 10:
                genre = "Fiction"
            case _:
                print ("Invalid Number!")
        pages_count = int(input("Pages Counts: "))
        print_count = int(input("Print Counts: "))
        book = Books (book_name, writer, genre, pages_count, print_count)
        book.add_book_in_database()
    case _:
        print ("Not Found!")

cnx.close ()