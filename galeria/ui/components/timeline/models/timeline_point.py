class TimelinePoint:
    def __init__(
        self,
        x: float,
        y: float,
        data=None,
        *,
        id: str | None = None,
        year: int | None = None,
        label: str = "",
        text: str = "",
    ):
        self.x = x
        self.y = y
        self.data = data or {}

        self.id = id or str(self.data.get("id") or self.data.get("label") or "")
        self.year = year if year is not None else self.data.get("year")
        self.label = label or str(self.data.get("label") or "")
        self.text = text or str(self.data.get("text") or "")
