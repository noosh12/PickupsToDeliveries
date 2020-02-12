import csv
import os
import sys
import re

class Order:
    def __init__(self, order_id, row):
        self.order_id = order_id
        if row[34]:
            self.shipping_name = row[34]
        else:
            self.shipping_name = row[24] # Use Billing Name if shipping name is empty
        self.address = row[36]
        self.city = row[39] # Suburb
        self.postcode = "".join(re.findall("\d+", row[40])) # numbers only
        self.phone = "".join(re.findall("\d+", row[43])) # numbers only
        self.notes = row[44]
        self.shipping_method = row[14]
    
    def get_output_string(self):
        return self.order_id + "," \
            + self.shipping_name + "," \
            + self.address + "," \
            + self.city + "," \
            + self.postcode + "," \
            + self.phone  + "," \
            + self.notes + "** Pickup Order added to deliveries **"

    def get_info(self):
        return self.order_id + "," \
            + self.shipping_name + "," \
            + self.phone  + "," \
            + self.notes  + "," \
            + self.shipping_method
    
    def get_shipping_method(self):
        return self.shipping_method

orders = {}
scanned = []

def main():
    verify_files_exist()
    process_csv_input()
    scan_orders()
    
    save_to_output = get_decision()
    if save_to_output:
        write_to_output()


def verify_files_exist():
    print("Searching for 'input.csv'... ")
    if os.path.isfile("input.csv"):
        print(" found.")
    else:
        print(' File not found! Exiting...')
        sys.exit()
    
    print("Searching for '_deliveries.csv'... ")
    if os.path.isfile("_deliveries.csv"):
        print(" found.")
    else:
        print(' File not found! Exiting...')
        sys.exit()
    print()


def write_to_output():
    print('Writing to output')
    with open('_deliveries.csv','a') as deliveries:
        for order_id in scanned:
            deliveries.write(orders[order_id].get_output_string() + '\n')
    print(' Success!')


def get_decision():
    if len(scanned) is 0:
        print('Exiting...')
        return False

    choice = 'placeholder'
    while choice.upper() is not 'Y' or 'N':
        choice = (input("To add, press 'y'. To cancel, press 'n': ")).upper()
        if choice == 'Y':
            return True
        elif choice == 'N':
            return False
        else:
            print('A valid selection has not been made.')
    

def scan_orders():
    while True:
        barcode = input('Scan a barcode or press enter to complete: ')

        if not barcode:
            break
        else:
            order_id = '#' + barcode
            if order_id in orders:
                print(orders[order_id].get_shipping_method().lower())
                if "delivery" in orders[order_id].get_shipping_method().lower():
                    print(" This is a delivery order. It will not be added")
                elif order_id in scanned:
                    print(" already scanned. Order to be added to deliveries once scanning is complete.")
                else:
                    scanned.append(order_id)
                    print(orders[order_id].get_info())
                    # print(order_id + " found. Order to be added to deliveries once scanning is complete.")
            else:
                print(order_id + ' is NOT in input file')
    print('\n'+str(len(scanned)) + ' valid orders scanned')


def process_csv_input():
    print('Processing input file...')
    prev_order_id = "placeholder"    
    with open('input.csv') as csv_file:
        
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

def create_order(order_id, row):
    orders[order_id] = Order(order_id, row)
    print('Order loaded: ' + orders[order_id].get_info())


if __name__ == "__main__":
    # execute only if run as a script
    main()