#conversion method for bool to string -
#aws returns bool for true false but tf requires this as a string
def bool_to_string(aws_bool):
    """Function to convert bool to string value."""
    if aws_bool:
        return "true"
    return "false"


def print_section_banner(text):
    """Function to print section banner."""
    print(f'############################### {text} ############################### ')
