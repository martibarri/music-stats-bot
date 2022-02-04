from typing import Optional

from sqlmodel import Field, SQLModel


class SocialMap:
    map = {
        "fb": "Facebook",
        "ig": "Instagram",
        "tw": "Twitter",
        "sp": "Spotify",
        "yt": "Youtube",
    }


class Social(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    dt: str
    fb: Optional[int] = 0
    ig: Optional[int] = 0
    tw: Optional[int] = 0
    sp: Optional[int] = 0
    yt: Optional[int] = 0


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    telegram_id: int
    username: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
