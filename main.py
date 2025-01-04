# imports (built-in)
import json
import datetime

# global
JSON_FILEPATH = 'data.json'
STATUS_DONE = 'mark-done'
STATUS_TODO = 'todo'
STATUS_IN_PROGRESS = 'mark-in-progress'
NUMBER_STR_IN_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DESCRIPTION = '''
What function would you like to do? 
1. Add task (add "")
2. Update task (update [session ID] "")
3. Delete task (delete [session ID])
4. Task Status Update - Mark 'In Progress' (mark-in-progress [session ID])
5. Task Status Update - Mark 'Done' (mark-done [session ID])
6. List All Task(s) (list)
7. List Task(s) by Status by 'done' (list done)
8. List Task(s) by Status by 'todo' (list todo)
9. List Task(s) by Status by 'in-progress' (list in-progress)
10. Type 'quit' to exit the program.
task-cli: '''

# loading json (if file found)
def loadFile(filepath: str):
    try: 
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            print('Successfully load of memory.')
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{filepath}' not found. Creating a new one.")
        data = []

# functions
def updateDateTime():
    return f'{datetime.datetime.now()}'[:-4] #hh:mm:ss:msms

def descriptionQuoteCorrection(string : str):
    return string.lstrip().replace("'","").replace('"',"") # extra space and quotes removed 

def quitText():
    print(f'User chose to save and quit program. '
          f'Thanks for using this task manager. '
          f'End of program.')

# This is bad however this was not a bug that crashs the program
def validateTaskID(user_input : str, json_data : list):

    options = [STATUS_DONE, STATUS_IN_PROGRESS, 'update', 'delete']

    if user_input.startswith((STATUS_DONE, STATUS_IN_PROGRESS, 'update', 'delete')):

        new_str_list = ''.join([user_input.removeprefix(opt).strip() 
                for opt in options if user_input.startswith(opt)])

        digit = ''
        for num in new_str_list:
            if num in NUMBER_STR_IN_LIST:
                digit += num
            else:
                break

        for dic in json_data:
            if (dic['id'] == int(digit)):
                # print(f'ID: {dic['id']} found')
                return True

        print(f"ID \'{int(digit)}\' not found")
    
    return True

# Status as None works here making the for if work with or without a status entered.
def displayTaskStatus(json_data : dict, status : str = None):
    for dic in json_data:
        if (dic['status'] == status) or (status is None):
            print(
                    f'\n'
                    f'ID: {dic['id']} - '
                    f'Description: {dic['description']} - '
                    f'Status: {dic['status'].upper()}'
                )

def addTasktoData(user_input : str, json_data : list):
    user_input = user_input.removeprefix('add')          
    print(f'Task Added; {user_input}')
    return json_data.append(
            { # Last ID found (most likely highest) + 1 or its becomes one with no data
            'id' : (json_data[-1]['id'] + 1) if len(json_data) > 0 else 1,
            'description' : descriptionQuoteCorrection(user_input), 
            'status' : 'todo',
            'createdAt' : updateDateTime(),
            'updatedAt' : updateDateTime()
        }
    )

def updateTaskData(user_input : str, json_data : list):
    user_input = user_input.removeprefix('update')
    id_number, updated_text = '', ''
    
    # to seperate the ID_number from the description            
    for num in user_input:
        if num in NUMBER_STR_IN_LIST:
            id_number += str(num)
        elif num not in NUMBER_STR_IN_LIST:
            break # preventing descripting numbers to be mixed with ID
            
    updated_text = user_input.replace(id_number, "")
    
    # updating description based on the correct ID
    for dic in json_data:
        if (dic['id'] == id_number):
            print(f'ID: {dic['id']} found')
            dic['description'] = descriptionQuoteCorrection(updated_text)
            dic['updatedAt'] = updateDateTime()
            print(f'Task Updated; {user_input}')
            break
     
    return json_data

def updateTaskStatus(user_input : str, json_data : list, mark_status : str):
    temp = user_input.replace(mark_status,'')
    id_number = int(temp)
    
    for dic in json_data:
        if (dic['id'] == id_number):
            dic['status'] = 'done' if mark_status[0:9] == 'mark-done' else 'in-progress'
            dic['updatedAt'] = updateDateTime()
            print(f'Task ID status has been updated.')
            break
        
    return json_data


def deleteTask(user_input : str, json_data : list):
    id_number = int(user_input.replace('delete',''))

    for index, dic_value in enumerate(json_data):
        if (dic_value['id'] == id_number):
            del json_data[index]
            print(f'Task ID status has been deleted.')
            break
        
    return json_data

# writing new data over old data
def saveFile(filepath: str, json_data : list):
    with open (filepath, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

    displayTaskStatus(json_data)
    print(f"Data successfully saved to {filepath}.")

# Main loop for running program
def main():
    data = loadFile(JSON_FILEPATH) # modularized to improve usability

    while True:
        user_input = input(DESCRIPTION).lower().strip()

        if not validateTaskID(user_input, data):
            continue

        if user_input.startswith('add'):
            addTasktoData(user_input, data)
        elif user_input.startswith('update'):
            updateTaskData(user_input, data)
        elif user_input.startswith('delete'):
            deleteTask(user_input, data)
        elif user_input.startswith('mark-in-progress'):
            updateTaskStatus(user_input, data, STATUS_IN_PROGRESS)
        elif user_input.startswith('mark-done'):
            updateTaskStatus(user_input, data, STATUS_DONE)
        elif user_input.startswith('list'):
            status = user_input.replace('list', '').strip()
            displayTaskStatus(data, status if status else None)
        elif user_input in ['quit', 'exit']:
            saveFile(JSON_FILEPATH, data)
            quitText()
            break

# making sure this is the only python file that runs
if __name__ == "__main__":
    main()
