# Code pair #p1
# Code B


def dump_stacks(signal=None, frame=None, file=sys.stdout):
    id_to_name = {
        thread.ident: thread.name for thread in threading.enumerate()
    }  # Changed id2name to id_to_name
    code = []
    for (
        thread_id,
        stack,
    ) in sys._current_frames().items():  # Changed threadId to thread_id
        code.append("\n# Thread: %s(%d)" % (id_to_name.get(thread_id, ""), thread_id))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    print("\n".join(code), file=file)
    if os.getenv("MITMPROXY_DEBUG_EXIT"):  # pragma: no cover
        sys.exit(1)
