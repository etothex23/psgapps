import PySimpleGUI as sg


class NoteWindow:
    def __init__(self) -> None:
        self.theme = 'aqua'
        self.lastx = None
        self.lasty = None
        self.layouts = {'draw_layout': [[sg.Canvas(background_color="#ffffff", size=(200, 200), pad=(5, 5),
                                                   key="DRAWPAD", tooltip="Draw here", visible=True,
                                                   border_width=3)],
                                        [sg.Text('Drawing Window')],
                                        [sg.Button('Read', button_color=("#000000", "#991a1a")),
                                         sg.Exit(button_color=("#000000", "#991a1a"))]]
                        }
        self.note = sg.Window('self.title_of_main', self.layouts['draw_layout'], ttk_theme=self.theme, finalize=True)
        self.DRAWPAD = self.note.Element("DRAWPAD")
        self.DRAWPAD.set_cursor('pencil')
        self.DRAWPAD.bind('<Button-1>', self.save_posn)
        self.DRAWPAD.bind("<B1-Motion>", self.draw_shape)
        self.key = None
        self.values = None
        self.event = 'Exit'

    def __repr__(self):
        return f'Window("{self.theme}","{self.lastx}","{self.lasty}","{self.key}", {self.values})'

    def __call__(self, event):
        '''Change the position of the entity.'''
        self.lastx, self.lasty = event

    def __get__(self, event, values):
        return self.values

    def __set__(self, event, values):
        self.values = values

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self.values[key]

    def __setitem__(self, key, values):
        self.values[key] = values

    def __delitem__(self, key):
        del self.values[key]

    def update(self, event, values):
        self.key = event
        self.values = values

    def note_go(self) -> None:
        print("Note go: ")
        print(self.event)
        print(self.note)
        print(self.DRAWPAD)
        while True:  # The Event Loop
            self.event, self.values = self.note.read()
            print("In the while: ")
            print(self.note)
            if self.event == sg.WIN_CLOSED or self.event == 'Exit':
                break

        self.note.close()

    def save_posn(self, event) -> None:
        print("save_posn: " + event)
        self.lastx, self.lasty = event.x, event.y

    def draw_shape(self, event) -> None:
        print("draw_shape: " + event)
        self.note['DRAWPAD'].create_line((self.lastx, self.lasty, event.x, event.y), fill='#000000')
        self.note['DRAWPAD'].save_posn(self, event)

    def clear_canvas(self) -> None:
        self.note['DRAWPAD'].delete("all")


NoteWindow().note_go()