from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import ConfigDict, field_validator
from pydantic import BaseModel


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: object) -> object:
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Title cannot be blank")
        if len(stripped_value) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped_value


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: object) -> object:
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Title cannot be blank")
        if len(stripped_value) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped_value


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    created_at: datetime
    updated_at: datetime
