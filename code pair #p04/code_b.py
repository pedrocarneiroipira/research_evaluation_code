# Code pair #p4
# Code B


@hybrid_property
def value(self):
    fieldname, _ = self.type_map[self.type]  # Removed unused variable 'discriminator'
    if fieldname is None:
        return None
    else:
        return getattr(self, fieldname)
