from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(default=1, description="Уникальный идентификатор пользователя")
    name: str = Field(default="John Doe", title="Имя пользователя", description="Полное имя")
    role: str = Field(default="user", alias="user_role", description="Роль пользователя в системе")
    
print(dict(User()))