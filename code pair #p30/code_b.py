# Code pair #p30
# Code B


def attach(self, filename=None, content=None, mimetype=None):
    """
    Attach a file with the given filename and content. The filename can
    be omitted and the mimetype is guessed, if not provided.

    If the first parameter is a MIMEBase subclass, insert it directly
    into the resulting message attachments.

    For a text/* mimetype (guessed or specified), when a bytes object is
    specified as content, decode it as UTF-8. If that fails, set the
    mimetype to DEFAULT_ATTACHMENT_MIME_TYPE and don't decode the content.
    """
    if not content and not isinstance(filename, MIMEBase):
        raise ValueError("content must be provided.")

    if isinstance(filename, MIMEBase):
        if content or mimetype:
            raise ValueError(
                "content and mimetype must not be given when a MIMEBase "
                "instance is provided."
            )
        self.attachments.append(filename)
    else:
        self._attach_file(filename, content, mimetype)


def _attach_file(self, filename, content, mimetype):
    mimetype = (
        mimetype or mimetypes.guess_type(filename)[0] or DEFAULT_ATTACHMENT_MIME_TYPE
    )
    basetype, _ = mimetype.split("/", 1)
    if basetype == "text" and isinstance(content, bytes):
        try:
            content = content.decode()
        except UnicodeDecodeError:
            mimetype = DEFAULT_ATTACHMENT_MIME_TYPE
    self.attachments.append(EmailAttachment(filename, content, mimetype))
