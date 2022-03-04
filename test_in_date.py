import PySimpleGUI as Sg
from datetime import datetime, timedelta

d_format = '%m/%d/%Y'
current_date = datetime.now()
days_to_add = 0
future_date = datetime.now()
past_date = datetime.now()

layout = [
    [Sg.Input(default_text=datetime.strftime(current_date, d_format), enable_events=True,
              s=12, key='-DATE-', pad=(10, 10), text_color='#e2f0c6',
              background_color='#323232', border_width=2, justification='right'),
     Sg.CalendarButton('Choose Date', target='-DATE-', key='-CALENDAR-', metadata='',
                       button_color=("#eeeeee", "#5c5c5c"), format='%m/%d/%Y')],
    [Sg.Text(' Days to +/-: ', text_color='#e2f0c6', background_color='#323232',
             pad=(10, 10), border_width=0, expand_x=True),
     Sg.InputText(default_text=0, s=5, key='-INPUT-', pad=(10, 10),
                  background_color='#ffffff', border_width=1, justification='right')]
]

calculator = Sg.Window(title='Calculator', layout=layout, background_color='#5c5c5c',
                       use_default_focus=True, element_justification='center',
                       element_padding=(10, 10), margins=(10, 10), finalize=True)

while True:  # Event Loop
    event, values = calculator.Read()
    if event == Sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-DATE-':
        #calculator['-INPUT-'].set_focus(force=True)
        print('x')
calculator.Close()
