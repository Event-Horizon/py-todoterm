from datetime import datetime
import json
import os
from modules.todoitem import TodoItem
from modules.todolist import TodoList


class TodoListSaveManager:
    """Class for saving and loading TodoList data."""
    
    def __init__(self, todo_list: TodoList, file_path: str = 'todos.json'):
        self.todo_list: TodoList = todo_list
        
        # Create an absolute path for the file based on the main script's directory
        self.file_path: str = os.path.abspath(file_path)

        # Connect to TodoList signals
        _ = self.todo_list.on_load.connect(self.load)
        _ = self.todo_list.on_changed.connect(self.save)

    def save(self, todo_list:TodoList):
        try:
            # Serialize the TodoList to JSON
            items_data = [
                {
                    'createdtime': item.createdtime.isoformat(),
                    'completedtime': item.completedtime.isoformat() if item.completedtime else None,
                    'text': item.text,
                    'completed': item.completed
                }
                for item in todo_list.get_list()  # Use the passed todo_list instance
            ]
            with open(self.file_path, 'w') as f:
                json.dump(items_data, f)
            # Generate Markdown file after saving
            self.generate_markdown()
        except IOError as e:
            print(f"Error saving todo list: {e}")


    def load(self, todo_list:TodoList):
        try:
            with open(self.file_path, 'r') as f:
                items_data = json.load(f)
                newlist = [
                    TodoItem(
                        createdtime=datetime.fromisoformat(item['createdtime']),
                        completedtime=datetime.fromisoformat(item['completedtime']) if item['completedtime'] else None,
                        text=item['text'],
                        completed=item['completed']
                    )
                    for item in items_data
                ]
                todo_list.set_list(newlist)
                self.todo_list = todo_list
        except FileNotFoundError:
            print("File not found. No items loaded.")
        except json.JSONDecodeError:
            print("Error decoding JSON. No items loaded.")
        except Exception as e:
            print(f"An error occurred while loading the todo list: {e}")
    
    def generate_markdown(self, markdown_file_path: str = 'todos.md'):
        """Generate a Markdown file from the JSON data."""
        try:
            with open(self.file_path, 'r') as f:
                items_data = json.load(f)

            with open(markdown_file_path, 'w') as md_file:
                _ = md_file.write("# Todo List\n\n")
                for item in items_data:
                    completed_status = "✓" if item['completed'] else "✗"
                    _ = md_file.write(f"- [{completed_status}] {item['text']} (Created: {item['createdtime']})\n")
                    if item['completedtime']:
                        _ = md_file.write(f"  - Completed on: {item['completedtime']}\n")
                # print(f"Markdown file '{markdown_file_path}' has been generated.")
        except FileNotFoundError:
            print("JSON file not found. Cannot generate Markdown.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Cannot generate Markdown.")
        except Exception as e:
            print(f"An error occurred while generating the Markdown file: {e}")