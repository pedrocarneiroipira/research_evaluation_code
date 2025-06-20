# Code pair #p1
# Code A


@hybrid_property
def value(self):
    fieldname, discriminator = self.type_map[self.type]
    if fieldname is None:
        return None
    else:
        return getattr(self, fieldname)