# Code pair #p13
# Code B


PROGRESS_ELAPSED_STYLE = "progress.elapsed"


def render(self, task: "Task") -> Text:
    """Show time elapsed."""
    elapsed = task.finished_time if task.finished else task.elapsed
    if elapsed is None:
        return Text("-:--:--", style=self.PROGRESS_ELAPSED_STYLE)
    delta = timedelta(seconds=max(0, int(elapsed)))
    return Text(str(delta), style=self.PROGRESS_ELAPSED_STYLE)
