class ErosionStatus:
    is_running: bool
    # signalize that the erosion (usually in other thread) should stop
    stop_requested: bool = False
    progress: int


    def __init__(self, is_running: bool = False, progress: int = 0):
        self.is_running = is_running
        self.progress = progress
