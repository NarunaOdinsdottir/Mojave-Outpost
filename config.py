# System-Limits
CPU_LIMIT = 80
RAM_LIMIT = 80
DISK_LIMIT = 90

# Sicherheits-Muster (Hier fügst du einfach neue Begriffe hinzu!)
SSH_FAIL_PATTERNS = [
    r"failed password",
    r"invalid user",
    r"connection closed by authenticating user",
    r"error",
    r"Connection closed by invalid user",
]

SQLI_PATTERNS = [
    r"UNION%20SELECT", 
    r"select.*from", 
    r"OR%201=1", 
    r"sleep\("
]
