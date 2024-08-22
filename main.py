from tkinter import messagebox
import random
from tkinter import *
import pyperclip
import json

SHORT_TEXT = 34
LONG_TEXT = 54
LONG_BUTT = 46
SHORT_BUTT = 15

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    pass_info.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    p_let = [random.choice(letters) for _ in range(random.randint(8, 10))]
    p_num = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    p_sym = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = p_let + p_num + p_sym
    random.shuffle(password_list)

    password = "".join(password_list)
    pass_info.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- Search Button ------------------------------- #


def find_password():
    text = web_info.get()
    with open("data.json", "r") as data_file:
        pass_data = json.load(data_file)
        try:
            if pass_data[text]:
                pass_disp = "Email: " + pass_data[text]["email:"] + "\nPasssword: " + pass_data[text]["password:"]
                messagebox.showinfo(title=text, message=f"{pass_disp}")
        except KeyError:
            messagebox.showerror(title="Website invalid", message=f"You do not have an entry for: {text}")
        else:
            web_info.delete(0, END)
            pass_info.delete(0, END)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    web_text = web_info.get()
    un_text = un_info.get()
    pass_text = pass_info.get()
    finished_text = f"{web_text} | {un_text} | {pass_text} \n"
    new_data = {
        web_text: {
            "email:": un_text,
            "password:": pass_text
        }

    }

    if len(web_text) == 0 or len(pass_text) == 0 or len(un_text) == 0:
        messagebox.showwarning(title="OOPS", message="Please make sure to fill in all of the fields!")
    else:
        is_ok = messagebox.askokcancel(title=web_text, message=f"These are the details entered: \nEmail: {un_text}"
                                                               f"\nPassword: {pass_text} \nIs this information correct?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            finally:
                web_info.delete(0, END)
                pass_info.delete(0, END)
                messagebox.showinfo(title="Task successful!", message="Your username and password have been "
                                                                  "saved successfully!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)


# BUTTONS #
gen_button = Button(text="Generate Password", width=SHORT_BUTT, command=generate_password)
gen_button.grid(column=2, row=3)

add_button = Button(text="Add", highlightthickness=0, width=LONG_BUTT, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=SHORT_BUTT, command=find_password)
search_button.grid(column=2, row=1)


# TITLES #
web_title = Label(text="Website:")
web_title.grid(column=0, row=1)

pass_title = Label(text="Password:")
pass_title.grid(column=0, row=3)

un_title = Label(text="Email/Username:")
un_title.grid(column=0, row=2)


# ENTRIES #
web_info = Entry(width=SHORT_TEXT)
web_info.grid(column=1, row=1)
web_info.focus()

un_info = Entry(width=LONG_TEXT)
un_info.insert(0, "testing.email@gmail.com")
un_info.grid(column=1, row=2, columnspan=2)

pass_info = Entry(width=SHORT_TEXT)
pass_info.grid(column=1, row=3)


window.mainloop()
