from PySimpleGUI import PySimpleGUI as sg

sg.theme('Dark BLue 11')
layout = [
    [sg.Text('WELCOME TO THE PYTHON ATM MACHINE',font='bold')],
    [sg.Text(f'Avaiable Values:\nR${50:.2f}\nR${20.:.2f}\nR${10:.2f}\nR${1:.2f}',font='bold')],
    [sg.Text('Withdraw Value: '),sg.Input(size=(10,1),key='value')],
    [sg.Button('Withdraw',key='withdraw')]]
window = sg.Window('cash machine', layout,size=(700,200))

while True:
    event, value = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'withdraw':
        withdraw = value['value']
        total = int(withdraw)
        dic = {}
        dic['notes of 50'] = 0
        dic['notes of 20'] = 0
        dic['notes of 10'] = 0
        dic['notes of 01'] = 0
        while True:
            if total>=50:
                total -= 50
                dic['notes of 50'] += 1
            elif total>=20:
                total -= 20
                dic['notes of 20'] += 1
            elif total>=10:
                total -= 10
                dic['notes of 10'] += 1
            elif total>=1:
                total -= 1
                dic['notes of 01'] += 1
            if total == 0:
                break
        layout_b = []
        for k,v in dic.items():
            if v !=0:
                print(k,v)
                layout_b.append([sg.Text(f'{k} R$ {v}')])
        window_b = sg.Window('Notes', layout_b,size=(200,200))

        while True:
            ev,va = window_b.read()
            if ev == sg.WINDOW_CLOSED:
                break
            

                                


               
