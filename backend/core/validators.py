import re


def iranian_phone_number_normalizer(phone: str) -> str:
    """
    Iranian phone numbers pattern are:
        - 09123456789
        - +989123456789
        - 00989123456789
        - 9123456789

    All of them should convert to standard pattern
    and then got saved!

    Standard pattern: 09123456789
    """

    phone = re.sub(r"\D", "", phone)

    # Strip country codes
    if phone.startswith("0098"):
        phone = "0" + phone[4:]
    elif phone.startswith("98"):
        phone = "0" + phone[2:]
    elif phone.startswith("9") and len(phone) == 10:
        phone = "0" + phone
    
    # Validate final format: 11 digits starting with 09
    if len(phone) == 11 and phone.startswith("09"):
        return phone
    
    return "Error"
