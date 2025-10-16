import re


def iranian_phone_number_normalizer(phone: str) -> str:
    """
    Iranian phone numbers are:
        - 09123456789
        - +989123456789
        - 00989123456789
        - 9123456789
    All of them should convert to standard pattern
    and then got saved!

    Standard pattern: 09123456789
    """

    phone = re.sub(r"\D", "", phone)

    if phone.startswith("0098"):
        phone = phone[4:]
    elif phone.startswith("98"):
        phone = phone[2:]
    elif phone.startswith("0"):
        pass
    else:
        phone = "0" + phone

    if len(phone) == 10 and not phone.startswith("0") and phone.startswith("9"):
        phone = "0" + phone
    else:
        return "Can't be normalized!"

    return phone
