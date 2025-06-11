import sys

from modules.todocommands import TodoCommand
from modules.todoitem import TodoItem
from modules.todolist import TodoList
from modules.todolist_savemanager import TodoListSaveManager

def parse_input(uinput:str) -> tuple[str,str|None] | None:
    result = uinput.split(" ",maxsplit=1)
    if len(result) < 1:
        return None
    if len(result) > 1:
        return (result[0],result[1])
    else:
        return (result[0],None)

def get_list(todo_list:TodoList)->str:
    result = ""
    eol = "\r\n"
    result += "Available Commands:"
    result += eol
    for command in TodoCommand:
        result +=  command.name + " "
    result += eol
    result += str(todo_list)
    return result

class TodoCommandsHandler(object):
    @staticmethod
    def handle_it(command_type:TodoCommand,command_value:str | None,todo_list:TodoList):
        match command_type:
            case TodoCommand.LIST:
                print(get_list(todo_list))
            case TodoCommand.NEW:
                print("Creating a new todo item.")
                if command_value:
                    todo_list.add_todo(TodoItem(text=command_value))
                else:
                    todo_list.add_todo(TodoItem())                
                print(get_list(todo_list))         
            case TodoCommand.TOGGLE:
                print("Toggling the todo item.") 
                if command_value and command_value.isdigit():
                    com_vint_t:int = int(command_value)-1
                    if com_vint_t >= len(todo_list) or com_vint_t < 0:
                        print(f"Invalid index {com_vint_t}, out of bounds.")
                    _ = todo_list.toggle_todo(com_vint_t)
                else:
                    print(f"Invalid index, not a digit.")                
                print(get_list(todo_list))
            case TodoCommand.DELETE:
                print("Deleting the todo item.")
                if command_value and command_value.isdigit():
                    com_vint_d: int = int(command_value)-1
                    if com_vint_d >= len(todo_list) or com_vint_d < 0:
                        print("Invalid index.")
                    _ = todo_list.delete_todo(com_vint_d)
                else:
                    print("Invalid index.")                
                print(get_list(todo_list))
            case TodoCommand.EXIT:
                print("Exiting the application.")
                sys.exit(0)
        
    


def run_loop() -> None:


    global_todolist = TodoList([TodoItem(text="Test!")])
    todo_list_manager = TodoListSaveManager(global_todolist)
    todo_list_manager.load(global_todolist)
    print(get_list(global_todolist))

    while True:
        user_input = input("> ")

        todo_command = None
        com_value = None

        command = parse_input(user_input)
        if command is not None:
            todo_command = command[0].upper()
            if command[1] is not None:
                com_value = command[1]

        if todo_command:

            # print(todo_command)

            try:
                match TodoCommand[todo_command]:
                    case TodoCommand.LIST:
                        TodoCommandsHandler.handle_it(TodoCommand.LIST,com_value,global_todolist)
                    case TodoCommand.NEW: 
                        TodoCommandsHandler.handle_it(TodoCommand.NEW,com_value,global_todolist)    
                    case TodoCommand.TOGGLE:
                        TodoCommandsHandler.handle_it(TodoCommand.TOGGLE,com_value,global_todolist)
                    case TodoCommand.DELETE:
                        TodoCommandsHandler.handle_it(TodoCommand.DELETE,com_value,global_todolist)
                    case TodoCommand.EXIT:
                        TodoCommandsHandler.handle_it(TodoCommand.EXIT,com_value,global_todolist)
                        break
                    case _:
                        print("Unknown command.")
            except KeyError:
                print("Unknown command.")

        



def main():
    run_loop()

if __name__ == "__main__":
    main()
# end main