import json


class Project:

    def __init__(self, name: str = "", command: str = "") -> None:
        self.name = name
        self.command = command

    def __repr__(self) -> str:
        return f"Project[{self.name=}, {self.command=}]"

    def to_json(self) -> str:
        return json.dumps(self)
