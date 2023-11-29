import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import tkinter.font as tkf

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="        ",
    database="school"
)
cursor = conn.cursor()

def execute_query(sql):
    try:
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_and_resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), resample = Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

def welcome_page():
    bgi = open_and_resize_image("/Users/evanimenon/Desktop/MySQLProject/welcomepage.png", 800, 500)
    bgl = tk.Label(welcome_frame, image=bgi)
    bgl.grid(row=0, column=0, sticky="nsew")
    bgl.image = bgi 
    welcome_frame.columnconfigure(0, weight=1)
    welcome_frame.rowconfigure(0, weight=1)
    menu_frame.pack_forget()

    abutton = tk.Label(welcome_frame, text="ADMIN", font=("Trebuchet MS", 16, "bold"), fg="black", bg="#86B1B8", bd=0, cursor="hand2")
    abutton.place(relx=0.795, rely=0.38, anchor="center")
    abutton.bind("<Button-1>", lambda event: admin_login_window())

    ubutton = tk.Label(welcome_frame, text="USER", font=("Trebuchet MS", 16, "bold"), fg="black", bg='White', bd=0, cursor="hand2")
    ubutton.place(relx=0.795, rely=0.65, anchor="center")
    ubutton.bind("<Button-1>", lambda event: user_login())

    welcome_frame.columnconfigure(0, weight=1)

def go_back_to_welcome(frame_to_hide):
    frame_to_hide.destroy()
    welcome_frame.pack(fill=tk.BOTH)

def admin_login_window():
    login_window_frame = tk.Frame(root, bg="#1F1E1F")
    login_window_frame.pack(fill=tk.BOTH, expand=True)

    back_button = tk.Button(login_window_frame, text="Back", font=("Trebuchet MS", 12), command=lambda: go_back_to_welcome(login_window_frame), bd=0)
    back_button.pack(anchor=tk.NW, padx=10, pady=10)
    tk.Label(login_window_frame, text="", bg="#1F1E1F", height=8).pack()

    password_label = tk.Label(login_window_frame, text="Password:", bg="#1F1E1F", font=custom_font)
    password_label.pack()
    password_entry = ttk.Entry(login_window_frame, show="*", font=custom_font, style="TEntry")
    password_entry.pack()

    tk.Label(login_window_frame, text="", bg="#1F1E1F", height=1).pack()
    login_button = tk.Button(login_window_frame, text="Login", command=lambda: admin_login(login_window_frame, password_entry), bg=button_bg, fg=button_fg, font=custom_font, bd=0)
    login_button.pack()

    welcome_frame.pack_forget()

def go_back_to_welcome(frame_to_hide):
    frame_to_hide.destroy()
    welcome_frame.pack(fill=tk.BOTH)

def admin_login(login_window_frame, password_entry):
    correct_password = "password"

    entered_password = password_entry.get()

    if entered_password == correct_password:
        login_window_frame.pack_forget()
        menu_frame.pack(fill=tk.BOTH, expand=True)
        reset_menu_layout()

        table_combobox.set("Details")
        table_combobox.pack(pady=10, side=tk.RIGHT, anchor=tk.SE)
        display_data("Details")
    else:
        messagebox.showerror("Incorrect Password", "The entered password is incorrect. Please try again.")


def reset_menu_layout():
    autofill_listbox.pack_forget()

    search_entry.pack(side=tk.TOP, padx=(10, 10))
    search_button.pack(side=tk.TOP, padx=(0, 10))

    view_data_button.pack(side=tk.LEFT, padx=(0, 10))
    update_data_button.pack(side=tk.LEFT, padx=(0, 10))
    add_data_button.pack(side=tk.LEFT, padx=(0, 10))
    delete_data_button.pack(side=tk.LEFT)

def user_login():
    welcome_frame.pack_forget()
    login_frame.pack_forget()
    menu_frame.pack(fill=tk.BOTH, expand=True)

    table_combobox.set("Details")
    table_combobox.pack(pady=10)

    # disable delete, update, add data button for user login
    delete_data_button.pack_forget()
    update_data_button.pack_forget()
    add_data_button.pack_forget()

    display_data("Details") 

    headings = get_table_columns("Details")
    tree["columns"] = headings
    for idx, heading in enumerate(headings):
        tree.heading(idx, text=heading)

    tree.column("#0", width=0)
    for idx, heading in enumerate(headings):
        tree.column(idx, width=tkf.Font().measure(heading) + 20)


def go_back_to_login():
    menu_frame.pack_forget()
    welcome_frame.pack(fill = tk.BOTH)

# function to display data in the form of a table
def display_data(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    for record in tree.get_children():
        tree.delete(record)

    headings = get_table_columns(table_name)
    tree["columns"] = headings

    for idx, heading in enumerate(headings):
        tree.heading(idx, text=heading)

    for col in tree["columns"]:
        tree.column(col, width=0)

    total_width = tree.winfo_width()
    column_width = int(total_width / len(headings))

    for idx, heading in enumerate(headings):
        tree.column(idx, width=column_width)

    for row in data:
        tree.insert("", "end", values=row)



def get_table_columns(table_name):
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = cursor.fetchall()
    return [column[0] for column in columns]

def delete_data():
    selected_item = tree.selection()

    if selected_item:

        sno = tree.item(selected_item, 'values')[0]
        table_name = table_combobox.get()

        if table_name:

            execute_query(f"DELETE FROM {table_name} WHERE sno = {sno}")
            messagebox.showinfo("Success", f"Record with Sno {sno} deleted from {table_name}")
            display_data(table_name)

        else:
            messagebox.showerror("Error", "Please select a table.")

    else:
        messagebox.showerror("Error", "Please select a record to delete.")

def update_data():
    selected_item = tree.selection()

    if selected_item:
        sno = tree.item(selected_item, 'values')[0]
        table_name = table_combobox.get()

        if table_name:
            update_window = tk.Toplevel(root)
            update_window.title("Update Data")

            columns = get_table_columns(table_name)
            entry_fields = []

            for idx, column in enumerate(columns):
                tk.Label(update_window, text=column).grid(row=idx, column=0)
                entry = tk.Entry(update_window)
                entry.grid(row=idx, column=1)
                entry.insert(0, tree.item(selected_item, 'values')[idx])
                entry_fields.append(entry)

            update_button = tk.Button(update_window, text="Update", command=lambda: perform_update(sno, table_name, columns, entry_fields, update_window))
            update_button.grid(row=len(columns), columnspan=2)

        else:
            messagebox.showerror("Error", "Please select a table.")
    else:
        messagebox.showerror("Error", "Please select a record to update.")

def perform_update(sno, table_name, columns, entry_fields, update_window):

    # sql query to update table with user input(set_values)
    set_values = ", ".join([f"{column} = '{entry.get()}'" for column, entry in zip(columns, entry_fields)])
    execute_query(f"UPDATE {table_name} SET {set_values} WHERE sno = {sno}")
    messagebox.showinfo("Success", f"Record with Sno {sno} updated in {table_name}")
    display_data(table_name)
    update_window.destroy()

def add_data():
    table_name = table_combobox.get()

    if table_name:
        add_window = tk.Toplevel(root)
        add_window.title("Add Data")

        columns = get_table_columns(table_name)
        entry_fields = []

        for idx, column in enumerate(columns):

            tk.Label(add_window, text=column).grid(row=idx, column=0)
            entry = tk.Entry(add_window)
            entry.grid(row=idx, column=1)
            entry_fields.append(entry)

        add_button = tk.Button(add_window, text="Add", command=lambda: perform_add(table_name, columns, entry_fields))
        add_button.grid(row=len(columns), columnspan=2)

    else:
        messagebox.showerror("Error", "Please select a table.")

def perform_add(table_name, columns, entry_fields):
    
    columns_str = ', '.join(columns)
    values_str = ', '.join([f"'{entry.get()}'" for entry in entry_fields])
    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"

    try:
        cursor.execute(sql)
        conn.commit()
        messagebox.showinfo("Success", f"Record added to {table_name} successfully!")
        display_data(table_name)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# function to perform the search operation
def perform_search():
    search_query = search_entry.get()

    if search_query:
        table_name = table_combobox.get()

        if table_name:
            # perform the SQL query and display the results
            query = f"SELECT * FROM {table_name} WHERE CONCAT({', '.join(get_table_columns(table_name))}) LIKE '%{search_query}%'"
            display_data_with_query(query)

        else:
            messagebox.showerror("Error", "Please select a table.")
    else:
        messagebox.showwarning("Warning", "Please enter a search query.")

# function to display data based on a custom SQL query
def display_data_with_query(query):
    try:
        cursor.execute(query)
        data = cursor.fetchall()

        for record in tree.get_children():
            tree.delete(record)
        for row in data:
            tree.insert("", "end", values=row)

        headings = [desc[0] for desc in cursor.description]
        tree["columns"] = headings
        for idx, heading in enumerate(headings):
            tree.heading(idx, text=heading)

        tree.column("#0", width=0)
        for idx, heading in enumerate(headings):
            tree.column(idx, width=tkf.Font().measure(heading) + 20)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# function to populate the autofill listbox based on the search query
def autofill():
    current_entry = search_entry.get().lower()
    autofill_listbox.delete(0, tk.END)
    query = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{conn.database}'
        AND column_name LIKE '{current_entry}%'
    """
    try:
        cursor.execute(query)
        suggestions = [result[0] for result in cursor.fetchall()]

        for suggestion in suggestions:
            autofill_listbox.insert(tk.END, suggestion)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def autofill_selected(event):
    selected_item = autofill_listbox.get(tk.ACTIVE)
    search_entry.delete(0, tk.END)
    search_entry.insert(0, selected_item)

# main application window
root = tk.Tk()
root.title("Student Database Management System")
root.geometry("800x500") 

root.resizable(0,0)

root.configure(bg="#1F1E1F")
button_bg = "#1F1E1F"
button_fg = "#000000"
custom_font = tkf.Font(family="Courier New", size=12) 

welcome_frame = tk.Frame(root,bg="#1F1E1F")
welcome_frame.pack(fill = tk.BOTH)

# admin login frame
login_frame = tk.Frame(root, bg="#1F1E1F")
password_label = tk.Label(login_frame, text="Password:", bg="#1F1E1F", font=custom_font)
password_entry = tk.Entry(login_frame, show="*", font=custom_font)
login_button = tk.Button(login_frame, text="Login", command=admin_login, bg=button_bg, fg=button_fg, font=custom_font,bd=0)

menu_frame = tk.Frame(root, bg="#1F1E1F")
menu_frame.pack(fill = tk.BOTH, expand = True)

welcome_page()

back_button = tk.Button(menu_frame, text = "Back", font = ("Trebuchet MS", 12), command = go_back_to_login,bd=0)
back_button.pack(anchor = "nw",padx=10,pady=10)

# search bar and autofill functionality
search_entry = tk.Entry(menu_frame, width=30, font=custom_font)
search_entry.pack(side=tk.TOP, padx=(10, 10))
search_button = tk.Button(menu_frame, text="Search", command=perform_search, bg=button_bg, fg=button_fg, font=custom_font,bd=0)
search_button.pack(side=tk.TOP, padx=(0, 10))

autofill_listbox = tk.Listbox(menu_frame, height=1, font=custom_font)
autofill_listbox.pack(side=tk.TOP, padx=(0, 10))
autofill_listbox.pack_forget()
autofill_listbox.bind('<<ListboxSelect>>', autofill_selected)
search_entry.bind('<KeyRelease>', lambda event: autofill())

# table selection combobox
tables = ["Details", "Marks", "Transport"]
table_combobox = ttk.Combobox(menu_frame, values=tables, font=custom_font, background=button_bg, foreground=button_fg)
table_combobox.pack(pady=10)
table_combobox.pack_forget()

# treeview to display data in the form of a table
tree = ttk.Treeview(menu_frame, columns=(), show="headings", height=15, style="Custom.Treeview")
tree.pack(pady=20, padx=20,fill=tk.BOTH, expand=True)

# view, update, add, delete data buttons
view_data_button = tk.Button(menu_frame, text="View Data", command=lambda: display_data(table_combobox.get()), bg=button_bg, fg=button_fg, font=custom_font, bd=0)
view_data_button.pack(side=tk.LEFT, padx=(0, 10))

update_data_button = tk.Button(menu_frame, text="Update Data", command=update_data, bg=button_bg, fg=button_fg, font=custom_font, bd=0)
update_data_button.pack(side=tk.LEFT, padx=(0, 10))

add_data_button = tk.Button(menu_frame, text="Add Data", command=add_data, bg=button_bg, fg=button_fg, font=custom_font, bd=0)
add_data_button.pack(side=tk.LEFT, padx=(0, 10))

delete_data_button = tk.Button(menu_frame, text="Delete Data", command=delete_data, bg=button_bg, fg=button_fg, font=custom_font, bd=0)
delete_data_button.pack(side=tk.LEFT)

root.mainloop()