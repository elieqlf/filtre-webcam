from dataclasses import dataclass


@dataclass
class AppState:
    gray: bool = False
    hat: bool = True
    mask: bool = True
    drop: bool = True
    smile: bool = True
    mirror: bool = True

    def toggle(self, attr: str):
        if hasattr(self, attr):
            setattr(self, attr, not getattr(self, attr))
