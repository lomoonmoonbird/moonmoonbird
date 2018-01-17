#--*-- coding: utf-8 --*--

from enum import Enum  # Needs package enum34
from enum import unique


@unique
class ErrorCodes(Enum):
    Ok = 0


    Forbidden = 0xFFFFFFFE
    DeviceHasBeenBanned = 0xFFFFFFFF
    BadRequest = 0x80000000
    InternalServerError = 0x7FFFFFFF
