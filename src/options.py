from enum import Enum


class OutputOption(str, Enum):
    MULTI_SHEET = "multi_sheet"
    SINGLE_SHEET = "single_sheet"


option_map = {
    "Multiple sheets": OutputOption.MULTI_SHEET,
    "Single sheet": OutputOption.SINGLE_SHEET,
}
