"""
UTILITY FUNCTIONS
"""


def validate_input_type(input_val, expected_t):
    try:
        valid_val = expected_t(input_val)
    except ValueError:
        valid_val = validate_input_type(input("the type of the input value is not right, please try again:"),
                                        expected_t)
    return valid_val


def text_to_dictionary(text: str):
    dictionary = {}
    kvpair_list = text.split("\n")
    for pair in kvpair_list:
        kvpair = pair.split(":")
        dictionary[kvpair[0].strip()] = kvpair[1].strip()
    return dictionary