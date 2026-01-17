def check_max_72_bytes(v: str) -> str:
    if v is None:
        raise ValueError("Password is required.")

    if not isinstance(v, str):
        v = str(v)

    b = v.encode("utf-8")
    if len(b) > 72:
        raise ValueError("Password must be at most 72 bytes (UTF-8).")
    return v
