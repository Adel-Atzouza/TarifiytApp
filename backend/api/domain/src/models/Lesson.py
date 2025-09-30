from pydantic import BaseModel

class Lesson(BaseModel):
    id: str
    title: str
    description: str