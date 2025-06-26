# Code pair #p22
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
    # This expects that GenerateJsonSchema was already used to generate the definitions
    json_schema = field_mapping[(field, override_mode or field.mode)]
    if "$ref" not in json_schema:
        # Set the title of the json schema based on the field's title or alias
        # This line will be removed in the future when Pydantic v1 is deprecated
        warnings.warn(
            "This line will be removed in the future when Pydantic v1 is deprecated",
            DeprecationWarning,
        )
        json_schema["title"] = field.field_info.title or field.alias.title().replace(
            "_", " "
        )
    return json_schema
