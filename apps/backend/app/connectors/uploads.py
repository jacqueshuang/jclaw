def normalize_uploaded_file(*, filename: str, content: str) -> dict[str, str]:
    """Map already-decoded upload input into the shared source shape.

    This helper does not parse files or extract text; callers must provide content.
    """
    return {
        "source_type": "upload",
        "title": filename,
        "content": content,
    }
