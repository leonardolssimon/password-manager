import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


WHITE = "#ffffff"
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #
def find_password():
    load_website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            loaded_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if load_website in loaded_data:
                loaded_email = loaded_data[load_website]["email"]
                loaded_password = loaded_data[load_website]["password"]
                messagebox.showinfo(title=load_website, message=f'Email: {loaded_email}\nPassword: {loaded_password}')
        else:
            messagebox.showinfo(title="Error", message=f"No details for {load_website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

canvas = Canvas(width=200, height=200, bg= WHITE, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#Labels
website_label = Label(text="Website:", bg=WHITE)
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", bg=WHITE)
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg=WHITE)
password_label.grid(column=0, row=3)

#Entries
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "leonardo.luisimon@hotmail.com")

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)


#Buttons
search_button = Button(text="Search", bg=WHITE, command=find_password, width=14)
search_button.grid(column=2, row=1, sticky="w")

pass_gen_button = Button(text="Generate Password", bg=WHITE, command=generate_password, width=14)
pass_gen_button.grid(column=2, row=3, sticky="w")

add_button = Button(text="Add", width=42, bg=WHITE, command=save)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()
