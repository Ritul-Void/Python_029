import json
import tkinter as tk 
from tkinter import messagebox
from difflib import get_close_matches


data = json.load(open("data.json"))

# Use the absolute path to the data.json file
file_path = "Enter the path of json file "



def access_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: !!Oops... I guess you missed to keep things in same folder!!")
        return {}
    except json.JSONDecodeError:
        print(f"Error: !!Oops... I think I am old i cant decode this file is it really json file you programi...!!")
        return {}
    
 
        
#finding correct match 
def translate(word, file):
    word = word.lower()
    if word in file:
        return file[word], None
    elif word.title() in file:
        return file[word.title()], None
    elif word.upper() in file:
        return file[word.upper()], None
    else:
        matches = get_close_matches(word, file.keys())
        if len(matches) > 0:
            return f"Did you mean '{matches[0]}' instead?", matches[0]
        else:
            return "The word does not exist. Please double-check it.", None

def on_search():
    word = entry.get().strip()
    if word:
        output, suggestion = translate(word, file)
        if isinstance(output, list):
            result_text = ' \n'.join(output)
        else:
            result_text = output
        result_label.config(text=result_text)
        
        if suggestion:
            def suggest():
                suggested_output = translate(suggestion, file)[0]
                result_label.config(text=suggested_output)
                suggest_button.pack_forget()

            suggest_button.config(command=suggest, text=f"Search for '{suggestion}'")
            suggest_button.pack()
        else:
            suggest_button.pack_forget()
    else:
        messagebox.showwarning("Input Error", "Please enter a word to search.")

#for data access
file = access_data(file_path)

#setting up GUI
root = tk.Tk()
root.title("Dictionary")

frame= tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label=  tk.Label(frame, text="Enter a word:")
label.pack()

entry = tk.Entry(frame, width=50)
entry.pack(pady=5)

search_button = tk.Button(frame, text="Search", command=on_search)
search_button.pack(pady=5)

result_label = tk.Label(frame, text="", wraplength=400, justify="left")
result_label.pack(pady=10)

suggest_button = tk.Button(frame, text="", wraplength=400, justify= "left")

root.mainloop()

#main body of the program
def main():    
      
    word = input("Enter the word you want to search: ")
    output = translate(word, file)
    if type(output) == list:
        for item in output:
            print(item)
    else:
        print(output)
        

if __name__ == "__main__":
    main()