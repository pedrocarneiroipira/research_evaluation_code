# Code pair #p1
# Code B



# refactored code
def spider_opened(self, _spider: Spider) -> None:
        self.time_prev: datetime = datetime.now(tz=timezone.utc)
        self.delta_prev: Dict[str, Union[int, float]] = {}
        self.stats_prev: Dict[str, Union[int, float]] = {}

        self.task = task.LoopingCall(self.log)
        self.task.start(self.interval)