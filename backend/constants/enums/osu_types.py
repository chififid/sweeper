from enum import unique, Enum


@unique
class OsuTypes(Enum):  # It's from kuriso
    INT8 = 0
    U_INT8 = 1
    INT16 = 2
    U_INT16 = 3
    INT32 = 4
    U_INT32 = 5
    FLOAT32 = 6
    INT64 = 7
    U_INT64 = 8
    FLOAT64 = 9
    BOOL = 10
    BYTE = 11

    MATCH = 12

    I32_LIST = 17
    I32_LIST4L = 18
    STRING = 19
    RAW = 20

