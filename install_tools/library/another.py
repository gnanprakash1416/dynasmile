import json
import os
# Define filename
def manage_item(file_name, item_key):
    # Check if the file exists
    if not os.path.isfile(file_name):
        # File does not exist, create it and initialize with empty items
        with open(file_name, 'w') as f:
            json.dump({"server": "", item_key: ""}, f)
        print(f"{file_name} file has been created with empty 'server' and '{item_key}'.")
        return 2
    else:
        # File exists, read its content
        with open(file_name, 'r') as f:
            data = json.load(f)
        # Check if the specified item exists
        if item_key not in data:
            # The item does not exist, add it with an empty value
            data[item_key] = ""
            with open(file_name, 'w') as f:
                json.dump(data, f)
            print(f"{item_key} has been added with an empty value.")
            return 3
        else:
            # The item exists, check its value
            if data[item_key] == "":
                # The item is empty, prompt the user for input
                new_item_value = input(f"{item_key} is empty. Please enter a value: ")
                data[item_key] = new_item_value
                with open(file_name, 'w') as f:
                    json.dump(data, f)
                print(f"{item_key} value has been saved.")
            else:
                # The item is not empty, ask the user if they want to modify it
                print(f"Current '{item_key}': {data[item_key]}")
                user_input = input("Do you want to modify it? (yes/no): ").strip().lower()
                if user_input == "yes":
                    new_item_value = input(f"Please enter a new value for '{item_key}': ")
                    data[item_key] = new_item_value
                    with open(file_name, 'w') as f:
                        json.dump(data, f)
                    print(f"'{item_key}' value has been modified and saved.")
                elif user_input == "no":
                    print("No modifications were made.")
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            return data[item_key]
    
    

if __name__=="__main__":
    file_name = 'server.json'
    # Call the function to manage the new item
    item_value=manage_item(file_name, "new item")
    print(f"{item_value}")
    manage_item(file_name, "server")