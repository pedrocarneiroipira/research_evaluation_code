# Code pair #p1
# Code A



def spider_opened(self, spider: Spider) -> None:
    self.time_prev: datetime = datetime.now(tz=timezone.utc)
    self.delta_prev: Dict[str, Union[int, float]] = {}
    self.stats_prev: Dict[str, Union[int, float]] = {}

    self.task = task.LoopingCall(self.log)
    self.task.start(self.interval)