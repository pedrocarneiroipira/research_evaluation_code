# Code pair #p1
# Code A


def get_multi_unique_constraints(
    self,
    connection,
    schema,
    filter_names,
    scope,
    kind,
    **kw,
):
    result = self._reflect_constraint(
        connection, "u", schema, filter_names, scope, kind, **kw
    )

    # each table can have multiple unique constraints
    uniques = defaultdict(list)
    default = ReflectionDefaults.unique_constraints
    for table_name, cols, con_name, comment, options in result:
        # ensure a list is created for each table. leave it empty if
        # the table has no unique cosntraint
        if con_name is None:
            uniques[(schema, table_name)] = default()
            continue

        uc_dict = {
            "column_names": cols,
            "name": con_name,
            "comment": comment,
        }
        if options:
            if options["nullsnotdistinct"]:
                uc_dict["dialect_options"] = {
                    "postgresql_nulls_not_distinct": options["nullsnotdistinct"]
                }

        uniques[(schema, table_name)].append(uc_dict)
    return uniques.items()
