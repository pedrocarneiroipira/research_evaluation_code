# Code pair #p1
# Code B



def decode(self, encoded):
    algorithm, _, algostr, work_factor, data = encoded.split("$", 4)
    assert algorithm == self.algorithm
    return {
        "algorithm": algorithm,
        "algostr": algostr,
        "checksum": data[22:],
        "salt": data[:22],
        "work_factor": int(work_factor),
    }