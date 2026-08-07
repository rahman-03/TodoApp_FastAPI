from pydantic import BaseModel, Field, ConfigDict

class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int  = Field(ge=1,le=5)
    complete : bool = False

class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : int
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int  = Field(ge=1,le=5)
    complete : bool = False

class DeleteAllTodosRequest(BaseModel):
    password: str = Field(min_length=8)