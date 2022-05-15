
""" Protocol CONSTANTS"""

CODE_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CODE_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol

SERVER_PROTOCOL = {
    'send_object': 'SEND_OBJECT'
}

CLIENT_PROTOCOL = {
    'request_object': 'REQUEST_OBJECT'
}


def join_data(data_fields, data_delimiter='#'):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like a#b#c
    """
    return data_delimiter.join(data_fields)


def split_data(data, expected_fields, data_delimiter='#'):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    data_fields = data.split(data_delimiter)

    if len(data_fields) == expected_fields:
        return data_fields

    return None


def pack_message(code, data):
    """
    Constructs a vaild message following this projects protocol given a code and data
    :param code: Protocol Code
    :param data: Protocol Data
    :return: A Valid message following the games protocol
    """
    if len(code) > CODE_FIELD_LENGTH:
        return None

    length = str(len(data))
    if len(length) > LENGTH_FIELD_LENGTH:
        return None

    if len(data) > MAX_DATA_LENGTH:
        return None

    # Pad code with whitespaces so length would be 16
    # for example: "LOGIN|" -> "LOGIN          |"
    message = code.ljust(CODE_FIELD_LENGTH) + DELIMITER

    # Pad length with zeros
    # for example: "4" -> "0004"
    message += length.zfill(LENGTH_FIELD_LENGTH) + DELIMITER

    # add data to message
    message += data
    return message


def unpack_message(message):
    """
    Parses a protocol message
    :param message: protocol message
    :return: code, data
    """

    message_fields = message.split(DELIMITER)

    if len(message_fields) == 3:
        code, length, data = message_fields
        # Remove whitespaces from code
        code = code.strip(" ")

        if len(length) == 4:

            # Remove all extra zeros
            if length == "0000":
                length = '0'
            else:
                length = length.lstrip('0')
                length = length.strip(' ')

            # Make sure that the given length is actually a number
            if length.isnumeric():
                if int(length) == len(data):
                    return code, data

    return None, None

""""def parse_message(data):
    ""
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    ""
    parsed = data.split(DELIMITER)
    if len(parsed) == 3:
        cmd, msg_len, msg = parsed
        # Remove all whitespaces and unnecessary zeros
        cmd = cmd.strip(" ")
        if len(msg_len) == 4:
            # Remove all whitespaces and unnecessary zeros
            # if msg_len is 0000 then the strip will remove all characters
            if msg_len != "0000":
                msg_len = msg_len.lstrip("0")
                msg_len = msg_len.strip(" ")
            else:
                msg_len = "0"

            if msg_len.isnumeric():
                if int(msg_len) == len(msg):
                    return cmd, msg

    return ERROR_RETURN, ERROR_RETURN
"""