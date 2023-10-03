import re

EMAIL_PATTERN = r'^([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.)?redttg\.com$'
    
def validate_email(email):
    match = re.match(EMAIL_PATTERN, email)
    
    if match:
        username = match.group(1)
        return username
    else:
        return None