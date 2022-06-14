from enum import IntFlag, unique


@unique
class RankedStatuses(IntFlag):  # It's from kuriso
    UNKNOWN = -2
    NOT_SUBMITTED = -1
    PENDING = 0
    NEED_UPDATE = 1
    RANKED = 2
    APPROVED = 3
    QUALIFIED = 4
    LOVED = 5
