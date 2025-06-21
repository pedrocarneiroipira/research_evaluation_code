# Code pair #p1
# Code B


def adjoin(space: int, *lists: list[str], **kwargs: Any) -> str:
    """
    Glues together two sets of strings using the amount of space requested.
    The idea is to prettify.

    ----------
    space : int
        number of spaces for padding
    lists : str
        list of str which being joined
    strlen : callable
        function used to calculate the length of each str. Needed for unicode
        handling.
    justfunc : callable
        function used to justify str. Needed for unicode handling.
    """
    str_len = kwargs.pop("strlen", len)
    just_func = kwargs.pop("justfunc", _adj_justify)

    new_lists = []
    lengths = [max(map(str_len, x)) + space for x in lists[:-1]]
    # not the last one
    lengths.append(max(map(len, lists[-1])))
    max_len = max(map(len, lists))
    for i, lst in enumerate(lists):
        adjusted_list = just_func(lst, lengths[i], mode="left")
        adjusted_list = ([" " * lengths[i]] * (max_len - len(lst))) + adjusted_list
        new_lists.append(adjusted_list)
    to_join = zip(*new_lists)
    return "\n".join("".join(lines) for lines in to_join)
