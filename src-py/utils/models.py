
from pydantic import BaseModel


class UserInformation(BaseModel):
    name: str
    nickname: str
    date_of_birth: str
    day: int
    month: int
    year: int
    nationality: str = None
    place_of_birth: str = None
    image_url: str = None
    bio: str = None
