from pydantic import BaseModel


# Базовая схема (общие поля)
class LocationBase(BaseModel):
    name: str
    address: str


# Схема для создания локации
class LocationCreate(LocationBase):
    pass


# Схема для чтения (возврат клиенту)
class LocationRead(LocationBase):
    id: int
    
    model_config = {"from_attributes": True}
