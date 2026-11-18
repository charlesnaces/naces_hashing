from sqlmodel import Field , SQLModel

class Users(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	username: str
	password: str

class Specs(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	windows:	str
	ram: 		str
	graphics:	str
	storage:	str
	processor:str
