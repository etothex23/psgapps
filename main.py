import tkinter
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import colorchooser
from datetime import timedelta, date


def onCanvasClick(event):
    print('Got canvas click', event.x, event.y, event.widget)


def onObjectClick(event):
    print('Got object click', event.x, event.y, event.widget, print(event.widget.find_closest(event.x, event.y)))


def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y


def drawShape(event):
    if ShowChoice() == 1:
        canvas.create_line((lastx, lasty, event.x, event.y), fill=Gccolor)
    elif ShowChoice() == 2:
        canvas.create_oval((lastx, lasty, event.x - 2, event.y - 2), fill=Gccolor)
    elif ShowChoice() == 3:
        canvas.create_rectangle((lastx, lasty, event.x - 4, event.y - 4), fill=Gccolor)
    elif ShowChoice() == 4:
        canvas.create_text(lastx, lasty, fill=Gccolor, font="Times 20 italic bold",
                           text="DEEZNUTZ")
    savePosn(event)


def ShowChoice():
    return v.get()


def clearCanvas():
    canvas.delete("all")


def colorChooser():
    global Gccolor
    color_code = colorchooser.askcolor(title="Choose color")
    tStyle.configure('cc.TLabel', foreground=color_code[1], background=color_code[1])
    Gccolor = color_code[1]


def addDate():
    new_date.set(date.today() + timedelta(days=input_text.get()))


def check_digit(d, i, P, s, S, v, V, W):
    if not isinstance(S, int) and len(P) > 3:
        input_text.set(s)
        print("In the top id:" + str(i) + " " + str(d) + " P:" + str(P) + " s:" + str(s) + " S:" + str(S) + " :trt:")
        return 0
    else:
        input_text.set(0)
        input_text.set(P)
        #date_text_in.delete(0,END)
        #date_text_in.insert(0, P)
        print("In the bottom id: " + str(i) + " " + str(d) + " P:" + str(P) + " s:" + str(s) + " S:" + str(S) + " :trt:")
        return 1


def slct(event):
    tStyle.configure("xx.TEntry", selectbackground="#F99D89", selectforeground="#000000")
    date_text_in.selection_range(0, END)


curr_date = date.today()

main_win = ThemedTk()
# main_win = Tk()
main_win.title('Notes')
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)

tStyle = ttk.Style()
tStyle.theme_use("aqua")
tStyle.configure("bb.TLabel", background="#CCCCCC", foreground="#000000", border="#ff0000",
                 relief=GROOVE, borderwidth=5, anchor=tkinter.S, width=12)
tStyle.configure("aa.TButton", anchor=tkinter.S)
tStyle.configure("xx.TEntry", relief=SUNKEN, justify=tkinter.RIGHT, width="5")
tStyle.configure('cc.TLabel', foreground="#000000", border="#ff0000", relief=GROOVE, width=5, borderwidth=3)
tStyle.configure('dd.TButton', width=10, justify=tkinter.RIGHT, relief=tkinter.RIDGE, borderwidth=3)

Gccolor = '#000000'
v = IntVar()
v.set(1)  # initializing the choice, i.e. Python
input_text = IntVar()  # Input to enter number of days to add
input_text.set(0)
new_date = StringVar()  # Text on new calculated date
new_date.set(curr_date)

Frcontent = ttk.Frame(main_win, padding=(5, 5, 15, 15))
Frcontent.grid(column=0, row=0, sticky=NSEW)
Frcontent.columnconfigure(0, weight=1)

Dframe = ttk.Frame(Frcontent, borderwidth=5, relief="ridge", width=800, height=600)
Dframe.grid(column=0, row=0, sticky=NSEW)

Sframe = ttk.Frame(Frcontent, borderwidth=2, relief="ridge", width=450, height=500)
Sframe.grid(column=1, row=0, sticky=NSEW)
Sframe.columnconfigure((0, 2, 3), weight=1)
Sframe.columnconfigure(1, weight=0)

canvas = Canvas(Dframe, cursor='pencil', width=800, height=600, background="white")
canvas.grid(column=0, row=0, sticky=NSEW)
canvas.bind("<Button-1>", savePosn)
canvas.bind("<B1-Motion>", drawShape)

valid_digit = Sframe.register(check_digit)
date_text_in = ttk.Entry(Sframe, textvariable=input_text, justify=tkinter.RIGHT, width=5, style="xx.TEntry",
                         validate="key", validatecommand=(valid_digit, '%d', '%i', '%P', '%s',' %S', '%v', '%V', '%W'))
date_text_in.bind("<FocusIn>", slct)

date_text_in.grid(column=1, row=0, sticky=SE)
datelbl = ttk.Label(Sframe, text=curr_date, style="bb.TLabel")
datelbl.grid(column=0, row=0, sticky=SE)
btnCalcDate = ttk.Button(Sframe, text="Calculate Date", command=addDate, style="aa.TButton")
btnCalcDate.grid(column=2, row=0, sticky=SE)
calculateddatelbl = ttk.Label(Sframe, text=curr_date, textvariable=new_date, style="bb.TLabel")
calculateddatelbl.grid(column=3, row=0, sticky=SE)

draw_type = [("Line", 1),
             ("Oval", 2),
             ("Rect", 3),
             ("Text", 4)]

colorlbl = ttk.Label(Sframe, text=" ", style="cc.TLabel")
colorlbl.grid(column=0, row=1, columnspan=1, sticky=SE)
namelbl = ttk.Label(Sframe, text="<-Chosen Color")
namelbl.grid(column=1, row=1, columnspan=1, sticky=SE)
btnColorChooser = ttk.Button(Sframe, text="Pick Color", command=colorChooser)
btnColorChooser.grid(column=2, row=1, columnspan=2, sticky=SE)
btnClear = ttk.Button(Sframe, text="Clear", width=7, command=clearCanvas, style="dd.TButton")
btnClear.grid(column=0, row=3, columnspan=2, sticky=tkinter.S)
btnCancel = ttk.Button(Sframe, text="Close", width=7, command=main_win.destroy)
btnCancel.grid(column=2, row=3, columnspan=2, sticky=tkinter.S)

rb = 0
for draw_type, val in draw_type:
    ttk.Radiobutton(Sframe,
                    text=draw_type,
                    variable=v,
                    command=ShowChoice,
                    value=val).grid(column=rb, row=2, sticky=(SE))
    rb += 1

main_win.mainloop()
