from src.constants import STATUS_CANCEL_ACCEPTED, STATUS_CANCEL_REJECTED
from src.helpers.utility import CancelUtility as utility 

class CancelService:

    def cancel_course(self, tbl_register, parts):
        course_registration_id = parts[1]

        if utility.cal_is_registration_cancelled(tbl_register, course_registration_id):
            updated_register = utility.cal_update_status(tbl_register, course_registration_id, 'CANCELLED')
            return f"{course_registration_id} {STATUS_CANCEL_ACCEPTED}"
        else:
            return f"{course_registration_id} {STATUS_CANCEL_REJECTED}"

