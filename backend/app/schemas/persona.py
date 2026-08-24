from pydantic import BaseModel


class PersonaOut(BaseModel):
    id: str
    name: str
    category: str
    description: str

    class Config:
        from_attributes = True