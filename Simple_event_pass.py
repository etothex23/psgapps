import PySimpleGUI as Sg
import pyautogui
import pygetwindow
from PIL import Image
import time
#from mss.darwin import MSS as mss
#import mss.tools

class NoteWindow:
    def __init__(self) -> None:
        self.win_pos = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
        self.lastx = None
        self.lasty = None
        self.layout = [[Sg.Canvas(background_color="#ffffff", size=(200, 200), pad=(0, 0),
                                  key="draw_pad", tooltip="Draw here", visible=True,
                                  border_width=3)],
                       [Sg.Text('Drawing Window')],
                       [Sg.Button('Read', button_color=("#000000", "#991a1a")),
                        Sg.Exit(button_color=("#000000", "#991a1a"))]]
        self.icon = "wm-logo.ico"
        self.note = Sg.Window('Drawpad', self.layout, ttk_theme='aqua', finalize=True)
        self.drawpad = self.note['draw_pad']
        self.key = None
        self.values = None
        self.event = 'Exit'

    def __str__(self):
        return f'Window {self.note} has properties {self.lastx} and {self.lastx}'

    def __repr__(self):
        return f'Window("{self.note}","{self.drawpad}","{self.layout}","{self.lastx}",' \
               f'"{self.lasty}","{self.key}","{self.values}",{self.event})'

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def init_canvas(self) -> None:
        print('init canvas')
        self.note.TKroot.iconbitmap(self.icon)
        # self.drawpad is the element which will be able to set the cursor
        self.drawpad.set_cursor('pencil')
        # self.note['draw_pad'].Widget get access to canvas
        self.note['draw_pad'].Widget.bind('<Button-1>', self.save_posn)
        self.note['draw_pad'].Widget.bind('<B1-Motion>', self.draw_shape)
        # self.note.TKroot get access to window
        # self.note.TKroot.bind('<Button-1>', self.save_posn)
        # self.note.TKroot.bind("<B1-Motion>", self.draw_shape)

    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y
        self.win_pos['x1'], self.win_pos['y1'] = self.note.TKroot.winfo_x(), self.note.TKroot.winfo_y()
        self.win_pos['x2'], self.win_pos['y2'] = self.note.TKroot.winfo_x() + 200 \
            , self.note.TKroot.winfo_y() + 200
        # print("save position")
        # print(event)
        # print(event.x, event.y)
        print(self.lastx, self.lasty)
        print(self.win_pos)

    def draw_shape(self, event):
        print("draw shape")
        # self.note['draw_pad'].Widget.create_line()
        self.drawpad.Widget.create_line((self.lastx, self.lasty, event.x, event.y), fill='#000000')
        self.save_posn(event)
        print(event.x, event.y)
        print(self.lastx, self.lasty)

    def clear_canvas(self) -> None:
        self.drawpad.delete("all")

    def save_image(self, filename='image-file.png'):
        savetime = time.strftime("%H_%M_%S", time.localtime())
        tit = pygetwindow.getAllTitles()
        print(tit)
        win = pygetwindow.getActiveWindow()
        print(win)
        xx, yy, wwidth, hheight = pygetwindow.getWindowGeometry(win)
        xx2 = xx + wwidth
        yy2 = yy + hheight
        pyautogui.screenshot('pyget-win.png')
        im = Image.open('pyget-win.png')
        im = im.crop((xx, yy, xx2, yy2))
        im.save('pyget-win.png')
        im.show('pyget-win.png')
        # with mss.mss() as mss_instance:  # Create a new mss.mss instance
        #     # The screen part to capture
        #     monitor = {"top": 760, "left": 460, "width": 200, "height": 200}
        #     output = savetime + "-{top}x{left}_{width}x{height}.png".format(**monitor)
        #     # Grab the data
        #     sct_img = mss_instance.grab(monitor)
        #     #mss_instance.shot(output=filename + '.png')
        #     # Save to the picture file
        #     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        #     print(output)
        print('done')

    def note_go(self) -> None:
        self.init_canvas()
        print("Note go: ")
        # print(self.event)
        # print(self.values)
        while True:  # The Event Loop
            self.event, self.values = self.note.read()
            if self.event == 'Read':
                self.save_image()
            if self.event == Sg.WIN_CLOSED or self.event == 'Exit':
                break

        self.note.close()


Note = NoteWindow()
Note.note_go()
