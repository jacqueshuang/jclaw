def normalize_uploaded_file(*, filename: str, content: str) -> dict[str, str]:
    return {
        "source_type": "upload",
        "title": filename,
        "content": content,
    }
