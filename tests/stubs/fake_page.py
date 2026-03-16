import asyncio


class FakePage:
    def __init__(self):
        self.controls = []
        self.overlay = []
        self.tasks = []
        self.scroll = None

    def add(self, *controls):
        self.controls.extend(controls)

    def update(self):
        pass

    def run_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        return task
