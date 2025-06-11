from blinker.base import NamedSignal
from datetime import datetime
from blinker import signal
from modules.todoitem import TodoItem
import humanize


class TodoList():
    """Class for keeping track of Todo's in a List."""

    # Signals for loading and changes
    on_load: NamedSignal = signal('on_load')
    on_changed: NamedSignal = signal('on_changed')

    def __init__(self,items:list[TodoItem]):
        self._list: list[TodoItem] = []  # instance variable
        if len(items) > 0:
            self._list = items
    
    def add_todo(self,item:TodoItem):
        self._list.append(item)
        _ = self.on_changed.send(self)

    def delete_todo(self,index:int):
        if index >= 0 and len(self._list) > index :
            _removed_item: TodoItem = self._list.pop(index)
            _ = self.on_changed.send(self)
            return True
        return False

    def toggle_todo(self,index:int):
        if index >= 0 and len(self._list) > index :
            self._list[index].completed = not self._list[index].completed
            self._list[index].completedtime = datetime.now()
            _ = self.on_changed.send(self)
            return True
        return False

    def get_list(self) -> list[TodoItem]:
        return self._list
    
    def set_list(self,items:list[TodoItem]) -> None:
        self._list = items

    def __str__(self) -> str: # pyright: ignore[reportImplicitOverride]
        result = "TodoList: "

        if not self._list:
            return result + "\r\nNo items in the list."

        for index, item in enumerate(self._list):
            result += "\r\n"
            
            # Validate createdtime
            if isinstance(item.createdtime, datetime):
                humanize_createdtime = humanize.naturaltime(datetime.now() - item.createdtime)
            else:
                humanize_createdtime = "ERROR"

            # Validate completedtime
            if item.completedtime and isinstance(item.completedtime, datetime):
                humanize_completedtime = humanize.naturaltime(datetime.now() - item.completedtime)
            else:
                humanize_completedtime = "N/A"

            result += f"{index + 1} : CREATED {humanize_createdtime} : {'DONE' if item.completed else 'PENDING'} : {humanize_completedtime} : {item.text}"

        return result
    
    def __len__(self):
        return len(self._list)