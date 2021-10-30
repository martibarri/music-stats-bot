from typing import Optional

from sqlmodel import Field, SQLModel


class Social(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    dt: str
    fb: int
    ig: int
    tw: int
    sp: int
    yt: int


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    telegram_id: int
    username: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
