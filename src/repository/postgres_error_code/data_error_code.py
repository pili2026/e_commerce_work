from enum import Enum


# For more error definitions, please refer to this link
# https://www.postgresql.org/docs/current/errcodes-appendix.html


class DataErrorCode(Enum):

    DATA_EXCEPTION = "22000"  # General data error such as value out of range.
    # Example: Attempting to insert the string 'twenty-five' into an integer column designed for age data.

    NUMERIC_VALUE_OUT_OF_RANGE = "22003"  # Numeric value exceeds the defined range of the column.
    # Example: Attempting to store the number 300 in a TINYINT column that only supports values from 0 to 255.

    STRING_DATA_RIGHT_TRUNCATION = "22001"  # String data is right truncated.
    # Example: Inserting a string into a varchar(10) column that is longer than 10 characters.
