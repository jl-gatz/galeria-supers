from galeria.ui.controllers import AutoTimeoutController


class AutoCloseBehavior:
    def __init__(self, seconds: int, on_timeout):
        self._controller = AutoTimeoutController(
            seconds=seconds,
            on_timeout=on_timeout,
        )

    def start(self):
        self._controller.start()

    def reset(self):
        self._controller.restart()

    def stop(self):
        self._controller.cancel()
