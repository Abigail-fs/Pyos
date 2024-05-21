from tkinter import *
from tkinter import ttk, messagebox
import turtle
import os
from os import listdir
from os.path import isfile, join

msb = messagebox
root = Tk()
login_window = ttk.Frame(root, padding=500)
username = "root"
password = "toor"
FILEPATH = os.environ.get("filepath")

def paint():

    def apply():
        turtle.pensize(int(brush_size_slider.get()))
        if brush_color_entry.get() != "":
            try:
                turtle.color(brush_color_entry.get())
            except turtle.TurtleGraphicsError:
                messagebox.showerror("error", f"{brush_color_entry.get()} is not a valid color.")

    drawing_settings_window = Toplevel(root)
    drawing_settings_window.config(height=100, width=100)
    brush_size_slider = Scale(drawing_settings_window, from_=1, to=10, orient=HORIZONTAL)
    brush_size_slider.grid(column=1, row=0)
    apply_button = Button(drawing_settings_window, text="Apply", command=apply)
    apply_button.grid(column=1, row=5)
    brush_size_label = Label(drawing_settings_window, text="Brush size:")
    brush_size_label.grid(column=0, row=0)
    brush_color_label = Label(drawing_settings_window, text="Color:")
    brush_color_label.grid(column=0, row=3)
    brush_color_entry = Entry(drawing_settings_window)
    brush_color_entry.grid(column=1, row=3)


    def go_to(x, y):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()

    def dragging(x, y):
        turtle.goto(x, y)

    screen = turtle.Screen()
    screen.title("Turtle Drawing Program")
    turtle.speed(0)
    turtle.pensize(int(brush_size_slider.get()))
    screen.onclick(go_to)
    turtle.ondrag(dragging)

    screen.mainloop()


def notepad_function(open_file_name=None):



    notepad_window = Toplevel(root)
    notepad_window.config(height=950, width=926)
    notepad_window.title("notepad")
    notepad_entry = Text(notepad_window, fg="black", bg="white", bd=10, height=50, width=100, font="ariel")
    notepad_entry.place(x=0, y=0)


    def save():
        text = notepad_entry.get("1.0", "end-1c")
        file_name = file_name_entry.get()
        if file_name != "":
            try:
                with open(f"text files/{file_name}", "r") as f:
                    if messagebox.askokcancel("Overwrite", f"{file_name} already exists.\n overwrite it?"):
                        with open(f"text files/{file_name}", "w") as file:
                            file.write(text)
                            messagebox.showinfo("success", "successfully saved file")
                            notepad_window.title(f"notepad - {file_name}")
                    else:
                        messagebox.showinfo("Canceled", "saving canceled")
            except FileNotFoundError:
                with open(f"text files/{file_name}", "w") as file:
                    file.write(text)
                    messagebox.showinfo("success", "successfully saved file")
                    notepad_window.title(f"notepad - {file_name}")
        else:
            messagebox.showerror(title="Empty field", message="You cannot leave the file name blank")

    def open_text_file():
        def open_file():
            text = open_file_entry.get()
            if text != "":
                try:
                    with open(f"text files/{text}", "r") as file:
                        file_contents = file.read()
                    notepad_entry.delete('1.0', 'end')
                    notepad_entry.insert("1.0", file_contents)
                    open_file_window.destroy()
                    notepad_window.title(f"notepad - {text}")
                except FileNotFoundError:
                    messagebox.showerror("File not found", "File was not found. Check the spelling and try again")
            else:
                messagebox.showerror(title="Empty field", message="You cannot leave the file name field empty")


        open_file_window = Toplevel(root)
        open_file_window.config(height=50, width=250)
        open_file_entry = ttk.Entry(open_file_window)
        open_file_entry.place(x=60, y=0)
        open_file_label = ttk.Label(open_file_window, text="File name:")
        open_file_label.place(x=0, y=0)
        open_file_button = ttk.Button(open_file_window, text="open", command=open_file)
        open_file_button.place(x=150, y=0)

    if open_file_name is not None:

        def open_file_any(file_name):

            text = file_name
            with open(f"text files/{text}", "r") as file:
                file_contents = file.read()
            notepad_entry.delete('1.0', 'end')
            notepad_entry.insert("1.0", file_contents)
            notepad_window.title(f"notepad - {text}")

    file_name_label = ttk.Label(notepad_window, text="Save as:")
    file_name_label.place(x=0, y=925)
    file_name_entry = ttk.Entry(notepad_window)
    file_name_entry.place(x=60, y=925)
    notepad_save_button = ttk.Button(notepad_window, text="save", command=save)
    notepad_save_button.place(x=190, y=925)
    open_button = ttk.Button(notepad_window, text="open", command=open_text_file)
    open_button.place(x=300, y=925)
    if open_file_name is not None:
        open_file_any(file_name=open_file_name)




def file_explorer():
    mypath = FILEPATH
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    files_window = Toplevel(root)
    file_num = 0
    for item in onlyfiles:
        file_num += 1
        button = ttk.Button(files_window, text=item, command=lambda i=item: notepad_function(i))
        button.grid(column=1, row=file_num)


def check_login():
    password_text = password_entry.get()
    username_text = username_entry.get()
    if password_text == password and username_text == username:
        login_window.destroy()
        home_window = ttk.Frame(root)
        home_window.config(height=100, width=100)
        login_button.grid_remove()
        username_entry.grid_remove()
        username_label.grid_remove()
        password_entry.grid_remove()
        password_label.grid_remove()
        text_editor_button = ttk.Button(text="Notepad", command=notepad_function)
        text_editor_button.grid(column=1, row=1)
        drawing_button = ttk.Button(text="Paint", command=paint)
        drawing_button.grid(column=2, row=1)
        files_button = ttk.Button(text="Files", command=file_explorer)
        files_button.grid(column=3, row=1)
    else:
        messagebox.showerror("Incorrect login", "Username or password incorrect")



login_window.grid()
login_button = ttk.Button(text="Login", command=check_login)
login_button.grid(column=0, row=3)
username_label = ttk.Label(text="Username:")
username_label.grid(column=0, row=1)
username_entry = ttk.Entry()
username_entry.grid(column=1, row=1)
password_label = ttk.Label(text="Password:")
password_label.grid(column=0, row=2)
password_entry = ttk.Entry()
password_entry.grid(column=1, row=2)

root.mainloop()
