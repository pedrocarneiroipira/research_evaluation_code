# Code pair #p1
# Code B


def get_schema_from_model_field(
    *,
    field: ModelField,
    schema_generator: GenerateJsonSchema,
    model_name_map: ModelNameMap,
    field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
    ],
    separate_input_output_schemas: bool = True,
) -> Dict[str, Any]:
    override_mode: Union[Literal["validation"], None] = (
        None if separate_input_output_schemas else "validation"
    )
    # Remove this logic when Pydantic v1 is fully deprecated.
    # Reference: https://github.com/pydantic/pydantic/blob/d61792cc42c80b13b23e3ffa74bc37ec7c77f7d1/pydantic/schema.py#L207
    json_schema = field_mapping[(field, override_mode or field.mode)]
    if "$ref" not in json_schema:
        json_schema["title"] = field.field_info.title or field.alias.title().replace(
            "_", " "
        )
    return json_schema
