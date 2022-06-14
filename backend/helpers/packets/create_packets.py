import struct
from typing import Any, Tuple

from constants.enums.osu_types import OsuTypes
from constants.enums.osu_packet_id import OsuPacketID


def write_int(value: int, byte_length: int, signed: bool) -> bytes:
    return value.to_bytes(byte_length, byteorder="little", signed=signed)


def write_byte(value: int) -> bytes:
    return write_int(value, 1, True)


def write_bytes(value: int) -> bytearray:
    return bytearray(value)


def write_u_int_8(value: int) -> bytes:
    return write_int(value, 1, False)


def write_int_8(value: int) -> bytes:
    return write_int(value, 1, True)


def write_u_int_16(value: int) -> bytes:
    return write_int(value, 2, False)


def write_int_16(value: int) -> bytes:
    return write_int(value, 2, True)


def write_u_int_32(value: int) -> bytes:
    return write_int(value, 4, False)


def write_int_32(value: int) -> bytes:
    return write_int(value, 4, True)


def write_u_int_64(value: int) -> bytes:
    return struct.pack("<Q", value)


def write_int_64(value: int) -> bytes:
    return struct.pack("<q", value)


def write_float(value: float) -> bytes:
    return struct.pack("<f", value)


def write_double(value: float) -> bytes:
    return struct.pack("<d", value)


def write_string(value: str) -> bytes:
    return value.encode(errors="ignore")


def write_bool(value: float) -> bytes:
    return bytes(1 if value else 0)


def write_variant(value: int) -> bytearray:
    arr = []
    length = 0
    while value > 0:
        arr.append(value & 0x7F)
        value >>= 7
        if value != 0:
            arr[length] |= 0x80
            length += 1

    return bytearray(arr)


def write_osu_string(value: str) -> bytearray:
    if len(value) == 0:
        arr = bytearray(write_byte(0))
    else:
        arr = bytearray(write_byte(11))
        arr.extend(write_variant(len(value.encode(errors="ignore"))))
        arr.extend(write_string(value))

    return arr


def write_u_leb_128(value: int) -> bytearray:
    return write_variant(value)


def write_i32_list(list_integers: Tuple[int, ...]) -> bytearray:
    arr = bytearray(write_u_int_16(len(list_integers)))

    for integer in list_integers:
        arr.extend(write_u_int_32(integer))

    return arr


def create_packet(pack_id: OsuPacketID, *args: Tuple[Any, OsuTypes]) -> bytes:
    packet_header = bytearray(struct.pack("<Hx", pack_id.value))  # Write package id to first two bytes
    packet_data = bytearray()

    ptypes = {  # It's from kuriso
        OsuTypes.I32_LIST: write_i32_list,
        OsuTypes.STRING: write_osu_string,
        OsuTypes.BYTE: write_byte,
        OsuTypes.BOOL: write_bool,
        OsuTypes.INT8: write_int_8,
        OsuTypes.U_INT8: write_u_int_8,
        OsuTypes.INT16: write_int_16,
        OsuTypes.U_INT16: write_u_int_16,
        OsuTypes.INT32: write_int_32,
        OsuTypes.U_INT32: write_u_int_32,
        OsuTypes.FLOAT32: write_float,
        OsuTypes.FLOAT64: write_float,
        OsuTypes.INT64: write_int_64,
        OsuTypes.U_INT64: write_u_int_64,
    }

    for packet, packet_type in args:
        writer = ptypes.get(packet_type, None)
        if not writer:
            continue  # Can't identify packet type

        packet_data.extend(writer(packet))

    pocket_len = bytearray(len(packet_data).to_bytes(4, signed=True, byteorder="little"))

    packet_array = bytes(packet_header + pocket_len + packet_data)

    return packet_array
