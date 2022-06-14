from enum import IntFlag, unique


@unique
class Privileges(IntFlag):  # It's from kuriso
    NORMAL = 0
    PLAYER = 1
    BAT = 2
    SUPPORTER = 4
    MOD = 6
    PEPPY = 8
    ADMIN = 16
    TOURNAMENT_STAFF = 32