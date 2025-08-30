
import enum

class TuitionStatus(enum.Enum):
    NOT_YET_PAID = "NOT_YET_PAID"
    PAID = "PAID"
    EXPIRED = "EXPIRED"
    IN_PROCESS = "IN_PROCESS"