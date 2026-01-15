def check_max_72_bytes(v: str) -> str:
    if v is None:
        raise ValueError("Password is required.")

    if not isinstance(v, str):
        v = str(v)

    b = v.encode("utf-8")
    if len(b) > 72:
        return b[:72].decode("utf-8", errors="ignore")
    return v
