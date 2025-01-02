# imports (built-in)
import json
import datetime

# global
JSON_FILEPATH = 'data.json'
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
try: 
    with open(JSON_FILEPATH, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
        print('successfully load of memory.')
except FileNotFoundError as e:
    print(f'{e}. Creating a new file.')
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

def displayAllTasks(json_data : dict):
    for dic in json_data: # possible one-liner but it looks weird
        print(
                f'\n'
                f'ID: {dic['id']} - '
                f'Description: {dic['description']} - '
                f'Status: {dic['status'].upper()}'
            )

def displayTaskStatus(json_data : dict, status : str):
    for dic in json_data:
        if dic['status'] == status:
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
            'id' : (json_data[-1]['id'] + 1) if len(data) > 0 else 1,
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
        if num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            id_number += str(num)
        elif num not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
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
    id_number = int(user_input.replace(mark_status,''))
    
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
def saveFile(json_data : list):
    with open (JSON_FILEPATH, 'w') as outfile:
        json.dump(json_data, outfile)

    displayAllTasks(json_data)

# Main loop for running program
def main():
    while True:
        user_input = input(DESCRIPTION)

        if (user_input[0:3] == 'add'):
            addTasktoData(user_input, data)
        elif (user_input[0:6] == 'update'):
            updateTaskData(user_input, data)
        elif (user_input[0:6] == 'delete'):
            deleteTask(user_input, data)
        elif (user_input[0:16] == 'mark-in-progress'):
            updateTaskStatus(user_input, data, 'mark-in-progress')
        elif (user_input[0:9] == 'mark-done'):
            updateTaskStatus(user_input, data, 'mark-done')
        elif (user_input == 'list'):
            displayAllTasks(data)
        elif (user_input == 'list done'):
            displayTaskStatus(data, 'done')
        elif (user_input == 'list todo'):
            displayTaskStatus(data, 'todo')
        elif (user_input == 'list in-progress'):
            displayTaskStatus(data, 'in-progress')
        elif (user_input in ['quit', 'exit']):
            quitText()
            saveFile(data)
            break

# making sure this is the only python file that runs
if __name__ == "__main__":
    main()
