# Code pair #p69
# Code A


def keypress(self, size: int, key: str):
    if key == "m_select":
        foc, idx = self.get_focus()
        signals.status_prompt_command.send(partial=foc.cmd.name + " ")
    elif key == "m_start":
        self.set_focus(0)
        self.walker._modified()
    elif key == "m_end":
        self.set_focus(len(self.walker.cmds) - 1)
        self.walker._modified()
    return super().keypress(size, key)
