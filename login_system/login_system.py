from PySimpleGUI import PySimpleGUI as sg
from urllib.request import urlopen
from sqlite3 import Error
import sqlite3

class RegisteredUser:
    def __init__(self,cpf,password):
        self.cpf = cpf
        self.password = password

class UnregisteredUser:
    def __init__(self, f_name, l_name, cpf, email,password):
        self.f_name = f_name
        self.l_name = l_name
        self.cpf = cpf
        self.email = email 
        self.password = password
        
def crud(sql_str,select = False):
    try:
        connection = sqlite3.connect('users.db')
    except sqlite3.Error as error:
        print(error)
    else:
        print('connected to db')
        cur = connection.cursor()
        cur.execute(sql_str)
        if not select:
            connection.commit()
            connection.close()
        else:
            result = cur.fetchall()
            return result
                
    
def login():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('CPF'), sg.Input(key = 'cpf',size=(24,1))],
        [sg.Text('Password'), sg.Input(key = 'password', password_char='x',size=(20,1))],
        [sg.Text('Are not a member? Join us'),sg.Button('Register', key = 'register')],
        [sg.Button('Sign-In',key='enter')]
        ]
        
    window = sg.Window('Login',layout,size=(500,150))

    while True:
        events, values =  window.read()
        if events == sg.WINDOW_CLOSED :
            break
        if events == 'enter':
            try_log = crud(f'''
            select * from users where CPF = '{values['cpf']}' and password = '{values['password']}';
            ''',select=True)
            if try_log != []:
                window.close()
                all_good()
                return True
            elif not try_log:
                window.close()
                register(fail_login=True)
                return False
        if events == 'register':
            window.close()
            register()
        
    
def register(fail_login = False):
    sg.theme('DarkAmber')
    if not fail_login:
        layout = [
            [sg.Text('Nice, welcome!\nRegistration page: ')],
            [sg.Text('First Name'), sg.Input(key = 'f_name',size=(24,1))],
            [sg.Text('Last Name'), sg.Input(key = 'l_name',size=(24,1))],
            [sg.Text('CPF'), sg.Input(key = 'cpf',size=(24,1))],
            [sg.Text('E-mail'), sg.Input(key = 'email',size=(24,1))],
            [sg.Text('Password'), sg.Input(key = 'password', password_char='x',size=(20,1))],
            [sg.Button('Register',key='register')]
            ]
        window = sg.Window('Register',layout,size=(500,300))    
    else:
        layout = [
            [sg.Text('We dont found your registration, please register or try again')],
            [sg.Button('Try Sign-In again', key='again')],
            [sg.Text('First Name'), sg.Input(key = 'f_name',size=(24,1))],
            [sg.Text('Last Name'), sg.Input(key = 'l_name',size=(24,1))],
            [sg.Text('CPF'), sg.Input(key = 'cpf',size=(24,1))],
            [sg.Text('E-mail'), sg.Input(key = 'email',size=(24,1))],
            [sg.Text('Password'), sg.Input(key = 'password', password_char='x',size=(20,1))],
            [sg.Button('Register',key='register')]
            ]
        window = sg.Window('Register',layout,size=(500,300))

    while True:
        events, values =  window.read()
        if events == sg.WINDOW_CLOSED :
            break
        if events == 'again':
            window.close()
            login()
        if events == 'register':
            user = UnregisteredUser(
            f_name= values['f_name'],
            l_name= values['l_name'],
            cpf = values['cpf'],
            email = values['email'],
            password = values['password'])
            try:
                crud(f''' insert into users values (
                    null,
                    '{user.f_name}',
                    '{user.l_name}',
                    '{user.cpf}',
                    '{user.email}',
                    '{user.password}');
                    ''')
            except sqlite3.IntegrityError:
                window.close()
                error_layout = [[sg.Text('OPS, CPF already exists')],
                [sg.Button('Back to login',key='back')]
                ]
                window = sg.Window('error', error_layout,size=(200,200))
                event,value = window.read()
                if event == 'back':
                    window.close()
                    login()
            else:
                window.close()
                ok_layout = [[sg.Text('Nice, you are registered')],
                [sg.Button('Back to login',key='back')]
                ]
                window = sg.Window('error', ok_layout,size=(200,200))
                event,value = window.read()

                if event == 'back':
                    window.close()
                    login()
            
            

def all_good():
    
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Login Successfully\nYou used a login system simulator!\nCreated by Renan Santana')],
        [sg.Button('Exit',key='exit')]
        ]

    window = sg.Window('All Good', layout)

    while True:
        events, values =  window.read()
        if events == sg.WINDOW_CLOSED :
            print (events)
            break
        if events == 'exit':
            window.close()
            
