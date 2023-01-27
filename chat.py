from tkinter import *
import customtkinter
import openai
import os
import pickle

root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry("600x420")
root.iconbitmap("ai_lt.ico")

# Color Scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def speak():
    if chat_entry.get():
        filename = "api_key"
        try:
            if os.path.isfile(filename):
                input_file = open(filename, 'rb')
                stuff = pickle.load(input_file)
                openai.api_key = stuff
                openai.Model.list()

                response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = chat_entry.get(),
                    temperature = 0,
                    max_tokens = 60,
                    top_p = 1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.0, 
                )

                my_text.tag_config('me', foreground = "LightSkyBlue")
                my_text.insert(END, "Me: " + chat_entry.get() , 'me')
                my_text.insert(END, "\n\n")
                my_text.insert(END, "ChatGPT: " + (response["choices"][0]["text"]).strip())
                my_text.insert(END, "\n\n")

            else:
                input_file = open(filename, 'wb')
                input_file.close()
                my_text.insert(END, "\n\nYou need an API Key to talk with ChatGPT.")
        except Exception as e:
            my_text.insert(END, f"\n\n There was an error\n\n{e}")
    else:
        my_text.insert(END, "\n\nHey! You forgot to type anything!")

def clear():
    my_text.delete(1.0, END)
    chat_entry.delete(0, END)

def key():
    root.geometry("600x580")
    api_frame.pack(pady=30)
    filename = "api_key"

    try:
        if os.path.isfile(filename):
            input_file = open(filename, 'rb')
            stuff = pickle.load(input_file)
            api_entry.insert(END, stuff)
        else:
            input_file = open(filename, 'wb')
            input_file.close()
    except Exception as e:
        my_text.insert(END, f"\n\n There was an error\n\n{e}")

def save_key():
    filename = "api_key"

    try:
        output_file = open(filename, 'wb')
        pickle.dump(api_entry.get(), output_file)

        api_entry.delete(0, END)

        api_frame.pack_forget()
        root.geometry("600x420")
    except Exception as e:
        my_text.insert(END, f"\n\n There was an error\n\n{e}")

#Text
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

my_text = Text(text_frame, 
    bg = "#343638",     
    width=65, 
    bd=1, 
    fg="#d6d6d6",
    relief = "flat",
    wrap=WORD,
    selectbackground="#1f538d")
my_text.grid(row=0, column=0)

text_scroll = customtkinter.CTkScrollbar(text_frame, command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

my_text.configure(yscrollcommand=text_scroll.set)

chat_entry = customtkinter.CTkEntry(root, 
    placeholder_text="Type Something to ChatGPT...",
    width=535,
    height=50,
    border_width=1)
chat_entry.pack(pady=10)

#Buttons
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

submit_button = customtkinter.CTkButton(button_frame,
    text = "Speak to ChatGPT",
    command = speak)
submit_button.grid(row=0, column=0, padx=15)

clear_button = customtkinter.CTkButton(button_frame,
    text = "Clear Response",
    command = clear)
clear_button.grid(row=0, column=1, padx=15)

api_button = customtkinter.CTkButton(button_frame,
    text = "Update API Key",
    command = key)
api_button.grid(row=0, column=2, padx=15)

#API
api_frame = customtkinter.CTkFrame(root, border_width = 1)
api_frame.pack(pady=10)

api_entry = customtkinter.CTkEntry(api_frame, 
    placeholder_text="Enter your API Key",
    width = 350, height = 50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

api_save_button = customtkinter.CTkButton(api_frame,
    text="Save key",
    command = save_key)
api_save_button.grid(row=0, column=1, padx=10)    

root.mainloop()