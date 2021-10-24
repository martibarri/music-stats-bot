from datetime import datetime


class SocialRow:
    def __init__(self, row: tuple) -> None:
        try:
            self.id = row[0]
            self.dt = datetime.strptime(row[1], "%Y%m%d_%H%M%S")
            self.fb = row[2]
            self.ig = row[3]
            self.tw = row[4]
            self.sp = row[5]
            self.yt = row[6]
        except Exception:
            self.id = None
            self.dt = None
            self.fb = None
            self.ig = None
            self.tw = None
            self.sp = None
            self.yt = None

    def __repr__(self):
        return f"<SocialRow {dict(self.__dict__.items())}>"

    def __str__(self):
        return f"<SocialRow {dict(self.__dict__.items())}>"


class UserRow:
    def __init__(self, row: tuple) -> None:
        self.id = row[0]
        self.telegram_id = row[1]
        self.username = row[2]
        self.first_name = row[3]
        self.last_name = row[4]

    def __repr__(self):
        return f"<UserRow {dict(self.__dict__.items())}>"

    def __str__(self):
        return f"<UserRow {dict(self.__dict__.items())}>"
