import datetime
from views import render_template
import re
from models import User, Phone



def checking_the_correct_bd_format(birthday,control_try_input_bd):
    time = False
    while time == False:
        try_format_bd = r"\d\d/\d\d/\d\d"
        isValidDate = True
        if birthday != '':
            if re.match(try_format_bd, birthday) is not None:
                day, month, year = birthday.split('/')
                try:
                    datetime.datetime(int(year), int(month), int(day))
                    time = True
                    control_try_input_bd = True
                    return control_try_input_bd

                except ValueError:
                    isValidDate = False
                if isValidDate == False:
                    print('The input of birth date is incorrect. \n')
                    print('Please, try again\n')
                    return control_try_input_bd
            else:
                print('The input of birth date is incorrect. \n')
                print('Please, try again\n')
                return control_try_input_bd
        else:
            time = True
            control_try_input_bd = True
            return control_try_input_bd

def menu_controller(data=None, cls=True):
    choice = "0"
    while choice != "7":
        render_template(context={}, template="menu.jinja2")
        choice = input("Type in a number (1-7): ")
        if choice == "1":
            all_users_controller(data=None, cls=True)
        elif choice == "2":
            add_user_controller(data=None, cls=True)
        elif choice == "3":
            update_controller(data=None, cls=True)
        elif choice == "4":
            delete_controller(data=None, cls=True)
        elif choice == "5":
            show_the_entry(data=None, cls=True)
        elif choice == "6":
            check_age(data=None, cls=True)
        elif choice != "7":
            print("Command was not found, please enter command from prompt below")
    render_template(context={}, template="exit.jinja2")
    exit()

def exit_controller(data=None, cls=True):
    render_template(context={}, template="exit.jinja2", cls=cls)
    exit()

def all_users_controller(data=None, cls=True):
    users = User.all()
    render_template(context={'users': users}, template="all_users.jinja2", cls=cls)
    return 'main', None  # (next state, data)

def add_user_controller(data=None, cls=True):
    render_template(context={}, template="user_first_name.jinja2", cls=cls)
    username = input()
    render_template(context={}, template="user_surname.jinja2", cls=cls)
    surname = input()
    render_template(context={}, template="user_nickname.jinja2", cls=cls)
    nickname = input()
    control_try_input_bd = False
    while control_try_input_bd == False:
        render_template(context={}, template="birthday.jinja2", cls=cls)
        birthday = input()
        if birthday !="":
            control_try_input_bd=checking_the_correct_bd_format(birthday,control_try_input_bd)
        else:
            control_try_input_bd = True
    name =  username.title()  # Автоматическое форматирование имени
    surname = surname.title()  # Автоматическое форматирование фамилии
    flag = False  # Проверка имени на уникальность
    users= User.all()
    for i in users:
        if i.name == name and i.surname == surname:
            flag = True
            break
    if flag == True:
        if_the_user_already_exists(data=None, cls=True)

    if flag == False :  # Если имя не нашли  дата верная
        user = User.add(name, surname, nickname, birthday)
        add_phone_controller(user, cls=True)


def add_phone_controller(user, cls=True):
    input_control = False
    while input_control == False:
        render_template(context={}, template="phone.jinja2", cls=cls)
        number = input()
        if number !="":
            number = number.replace('+7', '8')  # +7 -> 8 #Автоматическое форматирование номера
            if number[0] == '7':  # Если начинается с 7
                arr = '8'
                arr += number[1:]
                number = arr
            if len(number) == 10 and number[0] == 9:  # если остальная часть (без +7/8)
                arr = '8'
                arr += number[0:]
                number = arr
            if len(number) != 11:
                print('The input of number is incorrect.\n')
                print('Please, try again\n')
            else:
                phone = Phone.add(number, user)
                add_more_controller(user, cls=True)
                input_control = True
        else:
            print('The input of number is incorrect.\n')
            print('Please, try again\n')



def delete_controller(data=None, cls=True):
    render_template(context={}, template="delete_user.jinja2", cls=cls)
    choice = input()
    exit = False  # Небольшой костыль для выхода из цикла
    if choice == '1':  # Удаление по имени
        print('To do this please enter the following information:')
        name = input('Enter name >> ')
        surname = input('Enter surname >> ')
        users = User.all()
        flag = False  # Проверка имени, если есть - флаг true
        for i in users:
            if i.name == name and i.surname == surname:
                delete_user = i
                flag = True
                break

        while flag == False:  # Если не нашли человека
            render_template(context={}, template="couldn't find someone to delete.jinja2", cls=cls)
            choice = input()
            if choice == '1':
                delete_controller(data=None, cls=True)
                break
            elif choice == '2':
                break

        if flag == True:  # Если нашли - удаляем
            delete_user.delete(name, surname)
            print("\033[1mDeleted successfully\033[0m")

    if choice == '2':  # Удаление по номеру
        number_try = False
        while number_try == False:
            render_template(context={}, template="delete_number.jinja2", cls=cls)
            number = input()
            number = number.replace('+7', '8')  # +7 -> 8 #Автоматическое форматирование номера
            if number[0] == '7':  # Если начинается с 7
                arr = '8'
                arr += number[1:]
                number = arr
            if len(number) == 10 and number[0] == 9:  # если остальная часть (без +7/8)
                arr = '8'
                arr += number[0:]
                number = arr
            if len(number) != 11:
                print('The input of number is incorrect.\n')
            else:
                flag = False  # Проверка номера на наличие
                numbers = Phone.all()
                delete_numbers = []
                for i in numbers:
                    if i.phone == number:
                        delete_numbers.append(i.user_id)
                        flag = True
                if len(delete_numbers) >= 1:
                    users = []
                    for i in range(len(delete_numbers)):
                        users.append(User.search_by_ID(delete_numbers[i]))

                    correct_delete = False
                    correct_input = r'\d'
                    while correct_delete == False:
                        render_template(context={'users': users}, template="selecting_which_user_to_delete.jinja2",
                                        cls=cls)
                        answer = input()
                        if re.match(correct_input, answer) is not None:
                            answer = int(answer)
                            answer -= 1
                            users[answer].delete(users[answer].name, users[answer].surname)
                            correct_delete = True
                        else:
                            print('The input is incorrect. \n')
                            print('Please, try again\n')
                else:
                    while flag == False:  # Если не нашли человека
                        render_template(context={'users': users}, template=" could'nt_find_someone_delete_phone.jinja2",
                                        cls=cls)
                        choice = input()
                        if choice == '1':
                            delete_controller(data=None, cls=True)
                            break
                        elif choice == '2':
                            break
    else:
        menu_controller()





def update_number(user_update, cls=True):
    num_r = r'\d'
    input_control = False
    while input_control == False:
        render_template(context={}, template="update_number.jinja2")
        num = input()
        if re.match( num_r, num) is not None:
            num = int(num)
            num -=1
            render_template(context={}, template="phone.jinja2", cls=cls)
            number = input()
            if number != "":
                number = number.replace('+7', '8')  # +7 -> 8 #Автоматическое форматирование номера
                if number[0] == '7':  # Если начинается с 7
                    arr = '8'
                    arr += number[1:]
                    number = arr
                if len(number) == 10 and number[0] == 9:  # если остальная часть (без +7/8)
                    arr = '8'
                    arr += number[0:]
                    number = arr
                if len(number) != 11:
                    print('The input of number is incorrect.\n')
                    print('Please, try again\n')
                else:
                    user_numb= int(user_update.phones[num].phone)
                    phone = Phone.search_by_ID(user_update.id, user_numb)
                    phone.phone = number
                    input_control = True
                    print("\033[1mChanged successfully\033[0m")
            else:
                print('The input of number is incorrect.\n')
                print('Please, try again\n')



def update_controller(data=None, cls=True):
    render_template(context={}, template="update.jinja2", cls=cls)
    render_template(context={}, template="user_first_name.jinja2", cls=cls)
    name = input()
    name = name.title()
    render_template(context={}, template="user_surname.jinja2", cls=cls)
    surname = input()
    surname = surname.title()
    flag = False  # проверка имени
    users = User.all()
    for i in users:
        if i.name == name and i.surname == surname:
            user_update = i
            flag = True
            break
    if flag == False:
        render_template(context={}, template="if_there_is_no_user_in_the_database.jinja2", cls=cls)
        choice = input()
        if choice == '1':
            update_controller(data=None, cls=True)
        elif choice == '2':
            menu_controller()
        else:
            menu_controller()


    render_template(context={}, template="menu_update.jinja2", cls=cls)
    choice = input()

    if choice == '1':
        new_name = input("Enter new name >> ")
        user_update.name = new_name.title()
        print("\033[1mChanged successfully\033[0m")
        menu_controller()

    if choice == '2':
        new_surname = input("Enter new surname >> ")
        user_update.surname = new_surname.title()
        print("\033[1mChanged successfully\033[0m")
        menu_controller()


    if choice == '3':
        render_template(context={'user_update': user_update}, template="update_menu_number.jinja2", cls=cls)
        choice_1 = input()
        if choice_1 =="1":
            update_number(user_update)

        elif choice_1 =="2":
            add_phone_controller(user_update, cls=True)
        else:
            update_controller(data=None, cls=True)
    if choice == '4':
        control_try_input_bd = False
        while control_try_input_bd == False:
            new_db = input("Enter new birth date(DD/MM/YYYY input Format) >> ")
            control_try_input_bd= checking_the_correct_bd_format(new_db, control_try_input_bd)
            if control_try_input_bd == True:
                user_update.birthday = new_db
                print("\033[1mChanged successfully\033[0m")
                menu_controller()
        menu_controller()
    if choice == '5':
        new_nick= input("Enter new name >> ")
        user_update.nickname = new_nick.title()
        print("\033[1mChanged successfully\033[0m")
        menu_controller()
    else:
        menu_controller()


def if_the_user_already_exists(data=None, cls=True): # если пользователь уже есть в базе данных
    render_template(context={}, template="if_the_user_already_exists.jinja2", cls=cls)
    choice = input("Type in a number (1-3): ")
    if choice == '1':
        add_user_controller(data=None, cls=True)
    elif choice == '2':
        update_controller(data=None, cls=True)
    elif choice == '3':
        menu_controller()

def add_more_controller(user, cls=True):
    render_template(context={}, template="more_number.jinja2", cls=cls)
    answer = input()
    if answer == 'Y':
        add_phone_controller(user, cls=True)
    elif answer != 'N':
        print("Invalid response. Be more careful next time!")
    print("\033[1mChanged successfully\033[0m")
    return 51, user  # (next state, data)


def show_the_entry(data=None, cls=True):

    render_template(context={}, template="show_the_entry.jinja2", cls=cls)
    choice = input()
    if choice == "1":
        render_template(context={}, template="user_first_name.jinja2", cls=cls)
        name = input()
        users = User.all()
        name = name.title()
        users_show=[]
        flag = False  # Проверка имени, если есть - флаг true
        for i in users:
            if i.name == name:
                users_show.append(i)
                flag = True
                break

        while flag == False:  # Если не нашли человека
            render_template(context={}, template="couldnt_find_ni_odnogo.jinja2", cls=cls)
            choice_1 = input()
            if choice_1 == '1':
                show_the_entry()
                break
            elif choice_1 == '2':
                menu_controller()

        if flag == True:  # Если нашли - удаляем
            render_template(context={'users_show': users_show}, template="search_by_firstname.jinja2", cls=cls)
            render_template(context={}, template="meny_show_entry_2.jinja2", cls=cls)
            choice_2= input()
            if choice_2 =="1":
                show_the_entry()
            elif choice_2 == "2":
                menu_controller()
            else:
                print("Invalid input\n")
                show_the_entry()



    elif choice == "2":
        render_template(context={}, template="user_surname.jinja2", cls=cls)
        surname = input()
        users = User.all()
        surname =  surname.title()
        users_show = []
        flag = False  # Проверка имени, если есть - флаг true
        for i in users:
            if i. surname == surname:
                users_show.append(i)
                flag = True
                break

        while flag == False:  # Если не нашли человека
            render_template(context={}, template="couldnt_find_ni_odnogo.jinja2", cls=cls)
            choice_1 = input()
            if choice_1 == '1':
                show_the_entry()
                break
            elif choice_1 == '2':
                menu_controller()

        if flag == True:  # Если нашли - удаляем
            render_template(context={'users_show': users_show}, template="search_by_surname.jinja2", cls=cls)
            render_template(context={}, template="meny_show_entry_2.jinja2", cls=cls)
            choice_2 = input()
            if choice_2 == "1":
                show_the_entry()
            elif choice_2 == "2":
                menu_controller()
            else:
                print("Invalid input\n")
                show_the_entry()


    elif choice == "3":
        render_template(context={}, template="user_nickname.jinja2", cls=cls)
        nickname = input()
        users = User.all()
        surname =   nickname .title()
        users_show = []
        flag = False  # Проверка имени, если есть - флаг true
        for i in users:
            if i.nickname  ==  nickname :
                users_show.append(i)
                flag = True
                break

        while flag == False:  # Если не нашли человека
            render_template(context={}, template="couldnt_find_ni_odnogo.jinja2", cls=cls)
            choice_1 = input()
            if choice_1 == '1':
                show_the_entry()
                break
            elif choice_1 == '2':
                menu_controller()

        if flag == True:
            render_template(context={'users_show': users_show}, template="search_by_nickname.jinja2", cls=cls)
            render_template(context={}, template="meny_show_entry_2.jinja2", cls=cls)
            choice_2 = input()
            if choice_2 == "1":
                show_the_entry()
            elif choice_2 == "2":
                menu_controller()
            else:
                print("Invalid input\n")
                show_the_entry()


    elif choice == "4":
        input_control = False
        while input_control == False:
            render_template(context={}, template="phone.jinja2", cls=cls)
            number = input()
            number = number.replace('+7', '8')  # +7 -> 8 #Автоматическое форматирование номера
            if number[0] == '7':  # Если начинается с 7
                arr = '8'
                arr += number[1:]
                number = arr
            if len(number) == 10 and number[0] == 9:  # если остальная часть (без +7/8)
                arr = '8'
                arr += number[0:]
                number = arr
            if len(number) != 11:
                print('The input of number is incorrect.\n')
            else:
                users = User.all()
                users_show = []
                flag = False  # Проверка имени, если есть - флаг true
                for i in users:
                    for number_1 in i.phones:
                            if str(number_1) == number:
                                users_show.append(i)
                                flag = True
                                break

                while flag == False:  # Если не нашли человека
                    render_template(context={}, template="couldnt_find_ni_odnogo.jinja2", cls=cls)
                    choice_1 = input()
                    if choice_1 == '1':
                        show_the_entry()
                        break
                    elif choice_1 == '2':
                        menu_controller()

                if flag == True:
                    render_template(context={'users_show': users_show, 'number': number}, template="search_by_number.jinja2", cls=cls)
                    render_template(context={}, template="meny_show_entry_2.jinja2", cls=cls)
                    choice_2 = input()
                    if choice_2 == "1":
                        show_the_entry()
                    elif choice_2 == "2":
                        menu_controller()
                    else:
                        print("Invalid input\n")
                        show_the_entry()
                input_control = True



    elif choice == "5":
        control_try_input_bd = False
        while control_try_input_bd == False:
            render_template(context={}, template="birthday.jinja2", cls=cls)
            birthday = input()
            if birthday != "":
                control_try_input_bd = checking_the_correct_bd_format(birthday, control_try_input_bd)
            else:
                control_try_input_bd = True
        users = User.all()
        users_show = []
        flag = False  # Проверка имени, если есть - флаг true
        for i in users:
            if i.birthday  == birthday :
                users_show.append(i)
                flag = True
                break

        while flag == False:  # Если не нашли человека
            render_template(context={}, template="couldnt_find_ni_odnogo.jinja2", cls=cls)
            choice_1 = input()
            if choice_1 == '1':
                show_the_entry()
                break
            elif choice_1 == '2':
                menu_controller()

        if flag == True:
            render_template(context={'users_show': users_show}, template="search_by_bd.jinja2", cls=cls)
            render_template(context={}, template="meny_show_entry_2.jinja2", cls=cls)
            choice_2 = input()
            if choice_2 == "1":
                show_the_entry()
            elif choice_2 == "2":
                menu_controller()
            else:
                print("Invalid input\n")
                show_the_entry()

    elif choice !="6":
        menu_controller()
    menu_controller()






# elif choice == "3":
#         render_template(context={}, template="user_nickname.jinja2", cls=cls)
#         name = input()
#         name = name.title()
#         users = User.search_by_nickname()
#         render_template(context={'users': users}, template="search_by_nickname.jinja2", cls=cls)
#         render_template(context={}, template="menu_show_enty_2.jinja2", cls=cls)
#         choice_2 = input()
#         if choice_2 == "1":
#             show_the_entry()
#         elif choice_2 == "2":
#             menu_controller()
#         else:
#             print("Invalid input\n")
#             show_the_entry()
#     elif choice == "3":
#         render_template(context={}, template="user_nickname.jinja2", cls=cls)
#         name = input()
#         name = name.title()
#         users = User.search_by_number()
#         render_template(context={'users': users}, template="search_by_number.jinja2", cls=cls)
#         render_template(context={}, template="menu_show_enty_2.jinja2", cls=cls)
#         choice_2 = input()
#         if choice_2 == "1":
#             show_the_entry()
#         elif choice_2 == "2":
#             menu_controller()
#         else:
#             print("Invalid input\n")
#             show_the_entry()
#
#
#
#

def check_age(data=None, cls=True):
    while True:
        try:
            render_template(context={}, template="check_age.jinja2", cls=cls)
            render_template(context={}, template="user_first_name.jinja2", cls=cls)
            name = input()
            name = name.title()
            render_template(context={}, template="user_surname.jinja2", cls=cls)
            surname = input()
            surname = surname.title()
            is_found = False  # если нашли в базе
            user = User.search_by_name(name, surname)
            temp = user.birthday
            if temp == '':
                render_template(context={}, template="check_bd_menu.jinja2", cls=cls)
                choice = input()
                if choice == 1:
                    control_try_input_bd = False
                    while control_try_input_bd == False:
                        new_db = input("Enter new birth date >> ")
                        checking_the_correct_bd_format(new_db,control_try_input_bd)
                        if control_try_input_bd ==True:
                            user.birthday = new_db
                            print("\033[1mChanged successfully\033[0m")
                            menu_controller()
                else:
                    menu_controller()
            else:
                current_date = datetime.date.today()
                temp = temp.split('/')
                birthday = datetime.date(int(temp[2]), int(temp[1]), int(temp[0]))  # переводим в нужный формат
                age = current_date - birthday
                age = str(age)
                res = int(int(age.split()[0]) / 365)  # полное число лет
                print('\033[1m', end='')
                print(name, surname, 'is', res, 'years old now')
                print('\033[0m', end='')
                render_template(context={}, template="check_bd_menu_2.jinja2", cls=cls)
                choice = input()
                if choice == '1':
                    check_age(data=None, cls=True)
                if choice == '2':
                   menu_controller(data=None, cls=True)
        except:
            print("\033[1mIncorrect input, please try again\033[0m")