from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TodoItem():
    createdtime: datetime = field(default_factory=datetime.now) # force it to call NOW every instance creation
    completedtime: datetime | None = None
    text: str = ""
    completed: bool = False