# Code pair #p1
# Code A


def dump_stacks(signal=None, frame=None, file=sys.stdout):
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    print("\n".join(code), file=file)
    if os.getenv("MITMPROXY_DEBUG_EXIT"):  # pragma: no cover
        sys.exit(1)
