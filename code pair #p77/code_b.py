# Code pair #p1
# Code A


def run(self, args: List[str], opts: argparse.Namespace) -> None:
    # parse arguments
    if len(args) != 1 or not is_url(args[0]):
        raise UsageError()

    url = args[0]

    # prepare spidercls
    self.set_spidercls(url, opts)

    if self.spidercls and opts.depth > 0:
        self.start_parsing(url, opts)
        self.print_results(opts)
