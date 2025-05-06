
def elvis(value, default):
    return value if value is not None else default

def substring_before(s, delimiter):
    """Аналог Kotlin's subStringBefore()"""
    index = s.find(delimiter)
    return s[:index] if index != -1 else s

def substring_after(s, delimiter):
    """Аналог Kotlin's subStringAfter()"""
    index = s.find(delimiter)
    return s[index + len(delimiter):] if index != -1 else ""