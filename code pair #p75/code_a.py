# Code pair #p1
# Code A


def to_representation(self, value):
    assert "request" in self.context, (
        "`%s` requires the request in the serializer"
        " context. Add `context={'request': request}` when instantiating "
        "the serializer." % self.__class__.__name__
    )

    request = self.context["request"]
    format = self.context.get("format")

    # By default use whatever format is given for the current context
    # unless the target is a different type to the source.
    #
    # Eg. Consider a HyperlinkedIdentityField pointing from a json
    # representation to an html property of that representation...
    #
    # '/snippets/1/' should link to '/snippets/1/highlight/'
    # ...but...
    # '/snippets/1/.json' should link to '/snippets/1/highlight/.html'
    if format and self.format and self.format != format:
        format = self.format

    # Return the hyperlink, or error if incorrectly configured.
    try:
        url = self.get_url(value, self.view_name, request, format)
    except NoReverseMatch:
        msg = (
            "Could not resolve URL for hyperlinked relationship using "
            'view name "%s". You may have failed to include the related '
            "model in your API, or incorrectly configured the "
            "`lookup_field` attribute on this field."
        )
        if value in ("", None):
            value_string = {"": "the empty string", None: "None"}[value]
            msg += (
                " WARNING: The value of the field on the model instance "
                "was %s, which may be why it didn't match any "
                "entries in your URL conf." % value_string
            )
        raise ImproperlyConfigured(msg % self.view_name)

    if url is None:
        return None

    return Hyperlink(url, value)
