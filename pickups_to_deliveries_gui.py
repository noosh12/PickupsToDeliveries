import tkinter as tk
import os
from pickups_to_deliveries import *
from tkinter import filedialog
from tkinter import ttk

window = tk.Tk()
window.title('Pickups to Deliveries')
window.geometry("800x600")
input_filepath = ""
output_filepath = ""    

code = ''

def get_key(event):
    global code
    code += event.char
    if event.keysym == 'Return':
        print('result:', code)
        process_barcode(code.rstrip())
        code = ''

def browse_input_file():
    global input_filepath
    input_filepath = filedialog.askopenfilename()
    input_path.config(text=input_filepath)
    check_files()

def browse_output_file():
    global output_filepath
    output_filepath = filedialog.askopenfilename()
    output_path.config(text=output_filepath)
    check_files()

def check_files():
    delete_text()
    if input_filepath and output_filepath:
        process_input_button.config(state=tk.NORMAL)
        add_status_text("Ready to process input file..", "green", "black")
    elif not input_filepath:
        update_text("Please browse to input file.")
    elif not output_filepath:
        update_text("Please browse to output file.")


def add_status_text(status, background, foreground):
    delete_text()
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, status + "\n\n")
    text_area.tag_add("status", "1.0", "2.0")
    text_area.tag_config("status", background=background, foreground=foreground)
    text_area.config(state=tk.DISABLED)

def update_text(text):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.INSERT, text+"\n")
    text_area.config(state=tk.DISABLED)

def delete_text():
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.config(state=tk.DISABLED)

def get_started():
    window.bind('<Key>', get_key)
    global input_filepath
    global output_filepath
    input_filepath = ""
    output_filepath = ""
    
    update_text("Searching for 'input.csv'... ")
    if os.path.isfile("input.csv"):
        update_text(" found.\n")
        input_filepath = os.getcwd() + "/input.csv"
        input_path.config(text=input_filepath)
    else:
        update_text(' File not found! Please browse to input file.\n')
    
    update_text("Searching for '_deliveries.csv'... ")
    if os.path.isfile("_deliveries.csv"):
        update_text(" found.\n")
        output_filepath = os.getcwd() + "/_deliveries.csv"
        output_path.config(text=output_filepath)
    else:
        update_text(' File not found! Please browse to output file.\n')

    if input_filepath and output_filepath:
        process_input_button.config(state=tk.NORMAL)
        process_input()
        

def process_input():
    update_text("Processing input file...")
    process_csv_input()
    update_text(" done. " + str(len(orders)) + " Orders loaded\n")
    update_text("\nReady to scan...")
    window.bind('<Key>', get_key)
    input_button.config(state=tk.DISABLED)
    output_button.config(state=tk.DISABLED)
    process_input_button.config(state=tk.DISABLED)

    


def process_barcode(barcode):
    order_id = '#' + barcode
    delete_text()

    if (order_id) in orders:
        print(orders[order_id].get_shipping_method().lower())
        if "delivery" in orders[order_id].get_shipping_method().lower():
            print(" This is a delivery order. It will not be added")

            add_status_text("DELIVERY ORDER SCANNED. IT WILL NOT BE ADDED", "orange", "black")
            update_text(orders[order_id].get_formatted_info())
            update_text("\nCurrent total scanned: " + str(len(scanned)))
            update_text(str(scanned))
        elif order_id in scanned:
            print(" already scanned. Order to be added to deliveries once scanning is complete.")

            add_status_text("ALREADY SCANNED", "yellow", "black")
            update_text(orders[order_id].get_formatted_info())
            update_text("\nCurrent total scanned: " + str(len(scanned)))
            update_text(str(scanned))
        else:
            scanned.append(order_id)
            print(orders[order_id].get_info())

            add_status_text("ORDER FOUND!", "green", "black")
            update_text(orders[order_id].get_formatted_info())
            update_text("\nCurrent total scanned: " + str(len(scanned)))
            update_text(str(scanned))
            # print(order_id + " found. Order to be added to deliveries once scanning is complete.")
    else:
        print(order_id + " is NOT in input file")
        update_text(order_id + " is NOT in input file")
        add_status_text("Order " + order_id + " not found!", "red", "black")
        update_text("\nCurrent total scanned: " + str(len(scanned)))
        update_text(str(scanned))

def process_csv_input():
    global input_filepath
    print('Processing input file...')
    prev_order_id = "placeholder"    
    with open(input_filepath) as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            line_count += 1

            if line_count == 1: # headers row
                continue

            order_id = row[0]
            if order_id == prev_order_id: # same customer
                continue

            prev_order_id = order_id
            create_order(order_id, row)
            # print('Order ' + order_id + ' added')

    print(str(len(orders)) + ' Orders loaded successfully\n')

def write_to_output():
    if scanned:
        print('Writing to output')
        delete_text()
        add_status_text('Updating Output File',"blue","white")
        with open(output_filepath,'a') as deliveries:
            for order_id in scanned:
                update_text("Adding:\t"+orders[order_id].get_simple_info())
                deliveries.write(orders[order_id].get_output_string() + '\n')
        print(' Success!')
        update_text("\nSuccess!\nHave a nice day..")
        process_output_button.config(state=tk.DISABLED)
    else:
        add_status_text("No orders to add...", "red", "black")


file_labels = tk.Label(text = "..")
file_labels.grid(column=0, row=0)

input_label = tk.Label(text = "Browse to input file", anchor=tk.W, justify=tk.LEFT)
input_label.grid(column=0, row=2)
input_button = ttk.Button(text = "Browse", command=browse_input_file)
input_button.grid(column=5, row=2)
input_path = tk.Label(text = input_filepath,font=("Helvetica", 12))
input_path.grid(column=10, row=2)

output_label = tk.Label(text = "Browse to output file", anchor=tk.W, justify=tk.LEFT)
output_label.grid(column=0, row=3)
output_button = ttk.Button(text = "Browse", command=browse_output_file)
output_button.grid(column=5, row=3)
output_path = tk.Label(text = output_filepath,font=("Helvetica", 12))
output_path.grid(column=10, row=3)

process_input_button = ttk.Button(text = "Process Input", command=process_input)
process_input_button.grid(column=00, row=4)
process_input_button.config(state=tk.DISABLED)

process_output_button = ttk.Button(text = "Process Output", command=write_to_output)
process_output_button.grid(column=00, row=15)
process_input_button.config(state=tk.NORMAL)

text_area = tk.Text(master=window, bg="#FFFF99")
text_area.grid(column=0, row=6, columnspan=15, sticky = tk.W+tk.E)
text_area.config(state=tk.DISABLED, wrap=tk.WORD)

get_started()

# text_area2 = tk.Text(master=window, bg="#FFFF99")
# text_area2.grid(column=25, row=5, columnspan=5, sticky = tk.W+tk.E)
# text_area2.config(state=tk.DISABLED)



window.mainloop()