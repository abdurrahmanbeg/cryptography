import PySimpleGUI as sg
import pathlib
sg.ChangeLookAndFeel('BrownBlue')

WIN_W = 90
WIN_H = 25
file = None

menu_layout = [['File', ['Exit']],
              ['Encrypt', ['By file ... ', 'By text input', 'Encrypt key']],
              ['Decrypt', ['By file ... ', 'By text input', 'Decrypt key']]]

layout = [[sg.Menu(menu_layout)],
          [sg.Text('> New file <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
          [sg.Multiline(font=('Consolas', 12), size=(WIN_W/2, WIN_H/2), key='_BODY_')]]

window = sg.Window('Python Notepad - Hill Cipher', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True)
window.maximize()
window['_BODY_'].expand(expand_x=True, expand_y=True)


while True:
    event, values = window.read()
    if event in('Exit', None):
        break
    if event in ('By file ...'):
        print("File selected")
    if event in ('By text input'):
        print("Text input selected")
    if event in ('Encrypt key'):
        print("EnKey selected")
    if event in ('Decrypt key'):
        print("DeKey selected")
