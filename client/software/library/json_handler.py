import json


def append_tojson(filename: str, data: dict, data_if_blank=None):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        if data_if_blank != None:
            file_data = data_if_blank
        try:
            file_data["emp_details"].append(data)
        except KeyError:
            file_data = {"emp_details": [{"emp_name": "Nikhil",
                                         "email": "nikhil@geeksforgeeks.org",
                                          "job_profile": "Full Time"
                                          }]}
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def is_item_in_json(filename: str, item: str):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        for thing in file_data["emp_details"]:
            try:
                if thing['filename'] == item:
                    return True
            except:
                pass
        return False


def read_from_json(filename: str, key: str):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        for thing in file_data["emp_details"]:
            try:
                if thing['filename'] == key:
                    return thing
            except:
                pass


if __name__ == '__main__':
    y = {"emp_name": "Nikhil",
         "email": "nikhil@geeksforgeeks.org",
         "job_profile": "Full Time"
         }
    append_tojson('./test.json', y)
    print(is_item_in_json('test.json', "C:/Users/denti/Videos/1237187643.mp4"))
    print(read_from_json('test.json', "C:/Users/denti/Videos/1237187643.mp4"))
