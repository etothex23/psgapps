import PySimpleGUI as sg
from tkinter import colorchooser


class NoteWindow:
    def __init__(self, title="Main Title", theme="aqua", layout_type="pop_layout"):
        self.title_of_main = title
        self.theme = theme  # Keep things interesting for your users
        self.layout_type = layout_type
        self.last_position = {'x': 0, 'y': 0}
        self.pb_color = ['#000000', '#000000']
        self.layouts = {'pop_layout': [[sg.Text('Persistent window')],
                                       [sg.Input(key='-IN-')],
                                       [sg.Button('Read', button_color=("#000000", "#991a1a")),
                                        sg.Exit(button_color=("#000000", "#991a1a"))]],
                        'draw_layout': [[sg.Canvas(background_color="#ffffff", size=(200, 200), pad=(5, 5),
                                                   key="-DRAWPAD-", tooltip="Draw here", visible=True,
                                                   border_width=3)],
                                        [sg.Text('Drawing Window')],
                                        [sg.Button('Read', button_color=("#000000", "#991a1a")),
                                         sg.Exit(button_color=("#000000", "#991a1a"))]]
                        }
        self.note = sg.Window(self.title_of_main, self.layouts[layout_type], ttk_theme=self.theme, finalize=True)

    def set_cursor(self, which_element='-DRAWPAD-', cursor_type='pencil'):
        self.note[which_element].set_cursor(cursor_type, '#ff0000')

    def set_bindings(self, which_element='-DRAWPAD-'):
        print('set bindings')
        self.set_cursor()
        self.note[which_element].bind('<Button-1>', self.save_posn)
        #self.note[which_element].bind('<Button-1>', '', self.save_posn)
        self.note[which_element].bind("<B1-Motion>", self.draw_shape)

    def note_go(self, which_element='-DRAWPAD-'):
        if which_element == '-DRAWPAD-': self.set_bindings()
        print(self.last_position['x'])
        while True:  # The Event Loop
            event, values = self.note.read()
            print("im here :")
            print(event)
            print(values)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

        self.note.close()

    def on_canvas_click(self, event):
        self.last_position['x'], self.last_position['y'] = event.x, event.y
        print('Got canvas click', event.x, event.y, event.widget)
        print("hello")

    def on_object_click(self, event):
        self.last_position['x'], self.last_position['y'] = event.x, event.y
        print('Got object click', event.x, event.y, event.widget,
              print(event.widget.find_closest(event.x, event.y)))

    def save_posn(self, event):
        print('Got canvas click')
        self.last_position['x'], self.last_position['y'] = event.x, event.y


    def draw_shape(self, event, which_element='-DRAWPAD-'):
        self.note[which_element].create_line((self.lastx, self.lasty, event.x, event.y), fill=self.pb_color)
        # canvas.create_oval((lastx, lasty, event.x - 2, event.y - 2), fill=self.pb_color)
        # canvas.create_rectangle((lastx, lasty, event.x - 4, event.y - 4), fill=self.pb_color)
        # canvas.create_text(lastx, lasty, fill=self.pb_color, font="Times 20 italic bold", text="DEEZNUTZ")
        self.save_posn(self, event)

    def clear_canvas(self, which_element='-DRAWPAD-'):
        self.note[which_element].delete("all")

    def color_chooser(self, style_element):
        color_code = colorchooser.askcolor(title="Choose color")
        style_element.configure('cc.TLabel', foreground=color_code[1], background=color_code[1])
        self.pb_color = color_code[1]


NoteWindow(layout_type='draw_layout').note_go()
