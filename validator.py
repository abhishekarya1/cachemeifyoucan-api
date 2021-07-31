import validators


def validate_link(link):
    if link.strip() == "":
        return False
    elif validators.url(link) == True:
        return True
    else:
        return False

print(validate_link(link = "www.google.com"))        