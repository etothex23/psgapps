import tkinter
import PySimpleGUI as Sg
from datetime import datetime, timedelta


class DateCalculator:

    def __init__(self) -> None:
        self.d_format = '%m / %d / %Y'
        self.current_date = datetime.now()
        self.days_to_add = 0
        self.future_date = datetime.now()
        self.past_date = datetime.now()
        self.add_or_sub = True
        self.icon = "wm-logo.ico"
        self.r_font = ('Verdana', 12)
        self.h_font = ('Arial bold', 20)
        self.e = None
        self.v = None
        self.calc_layout = [[Sg.Text('Current Date: ', text_color='#e2f0c6', background_color='#323232',
                                     pad=(10, 10), border_width=0, expand_x=True),
                             Sg.Input(self.getsdate(), 12, key='-DATE-', enable_events=True, pad=(10, 10),
                                      text_color='#e2f0c6', background_color='#323232', border_width=2,
                                      justification='right'),
                             Sg.CalendarButton('Choose Date', target='-DATE-', key='-CALENDAR-', metadata='',
                                               button_color=("#eeeeee", "#5c5c5c"), format=('%m / %d / %Y'))],
                            [Sg.Text(' Days to +/-: ', text_color='#e2f0c6', background_color='#323232',
                                     pad=(10, 10), border_width=0, expand_x=True),
                             Sg.Input(0, 5, key='-INPUT-', enable_events=True, pad=(10, 10),
                                      background_color='#ffffff', border_width=1, justification='right')],
                            [Sg.Text('Past Date: ', text_color='#e2f0c6', background_color='#323232',
                                     pad=(10, 10), border_width=0, expand_x=True),
                             Sg.Text(self.getsdate('p'), text_color='#ecf5da', background_color='#323232', pad=(10, 10),
                                     key='pdate', border_width=2, relief='sunken')],
                            [Sg.Text('Future Date: ', text_color='#e2f0c6', background_color='#323232',
                                     pad=(10, 10), border_width=0, expand_x=True),
                             Sg.Text(self.getsdate('f'), text_color='#ecf5da', background_color='#323232', pad=(10, 10),
                                     key='fdate', border_width=2, relief='sunken')]]
        self.layout = [[Sg.Text('Date Calculator', justification='c', font=self.h_font, size=(15, 1),
                                relief='ridge', border_width=2, text_color='#cde59e', background_color='#323232')],
                       [Sg.Frame(title='Calculate date:', title_color='#cde59e', title_location=Sg.TITLE_LOCATION_TOP,
                                 layout=self.calc_layout, border_width=2, pad=(10, 10),
                                 background_color='#3a3a3a', element_justification='right', expand_x=True)],
                       [Sg.Button('Calc', key='-CALC-', button_color=("#eeeeee", "#3a3a3a")),
                        Sg.Exit(button_color=("#eeeeee", "#3a3a3a"))]]
        self.calculator = Sg.Window('Calculator', self.layout, icon=self.icon, background_color='#5c5c5c',
                                    element_justification='center', element_padding=(10, 10),
                                    margins=(10, 10), font=self.r_font, finalize=True)

    def getsdate(self, t='c'):
        if t == 'p':
            return datetime.strftime(self.past_date, self.d_format)
        elif t == 'f':
            return datetime.strftime(self.future_date, self.d_format)
        else:
            return datetime.strftime(self.current_date, self.d_format)

    def getddate(self, datetoparse):
        return datetime.strptime(datetoparse, self.d_format)

    def select_text(self, event=None):
        self.calculator['-INPUT-'].Widget.config(background='#edffd3')
        self.calculator['-INPUT-'].Widget.selection_range(0, 'end')
        self.calculator['-INPUT-'].set_focus(force=True)

    def change_back(self):
        self.calculator['-INPUT-'].Widget.config(background='#ffffff')

    def set_and_calc(self):
        self.current_date = self.getddate(self.calculator['-DATE-'].get())
        self.future_date = self.current_date + timedelta(days=self.days_to_add)
        self.past_date = self.current_date + timedelta(days=-self.days_to_add)
        self.calculator['fdate'].update(self.getsdate('f'))
        self.calculator['pdate'].update(self.getsdate('p'))

    def init_date_calc(self):
        self.calculator['-INPUT-'].Widget.bind('<Button-1>', self.select_text)

    def exec_calc(self) -> None:
        self.init_date_calc()
        self.select_text()
        while True:  # The Event Loop
            self.e, self.v = self.calculator.read()
            temp = self.v['-INPUT-']
            if self.e == Sg.WIN_CLOSED or self.e == 'Exit':
                break
            elif self.e == '-INPUT-':
                if not temp.isdigit():
                    self.calculator['-INPUT-'].update(0)
                    self.select_text()
                elif temp.isdigit():
                    if temp[0] == '0':
                        self.select_text()
                    else:
                        self.change_back()
                        self.days_to_add = int(temp)
                        self.set_and_calc()
            elif self.e == '-CALC-':
                self.days_to_add = int(temp) if temp.isdigit() else 0
                self.set_and_calc()
            elif self.e == '-DATE-':
                self.select_text()
                self.set_and_calc()

        self.calculator.close()


DateCalculator().exec_calc()
