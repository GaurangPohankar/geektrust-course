from src.constants import *
from src.helpers.utility import get_current_date, find_course_by_id, allot_is_course_cancelled, update_statuses

class AllotService:

    def allot_course(self, tbl_course, tbl_register, parts):
        course_offering_id = parts[1]
        current_date = get_current_date()

        course = find_course_by_id(tbl_course, course_offering_id)
        if not course:
            return INPUT_ERROR

        registration_count = self.get_registration_count(tbl_register, course_offering_id)

        course_status = STATUS_ONLINE
        if self.is_course_cancelled(course, current_date, registration_count, course['minEmployee']):
            course_status = STATUS_CANCELLED
            course['status'] = STATUS_CANCELLED

        updated_entries = self.update_registration_statuses(tbl_register, course_offering_id, course_status)
        updated_entries.sort(key=lambda entry: entry['course_registration_id'])

        alloted_str = self.format_alloted_entries(updated_entries, course)

        return alloted_str

    def get_registration_count(self, tbl_register, course_offering_id):
        return sum(
            1 for registration in tbl_register
            if registration['course_offering_id'] == course_offering_id
            and (registration['status'] == STATUS_PENDING or registration['status'] == STATUS_CONFIRMED)
        )

    def is_course_cancelled(self, course, current_date, registration_count, min_course_limit):
        return allot_is_course_cancelled(course, current_date, registration_count, min_course_limit)

    def update_registration_statuses(self, tbl_register, course_offering_id, course_status):
        return update_statuses(tbl_register, course_offering_id, course_status)

    def format_alloted_entries(self, updated_entries, course):
        return "\n".join(
            f"{entry['course_registration_id']} {entry['email']} {course['course_offering_id']} {course['course_name']} "
            f"{course['instructor']} {course['date']} {entry['status']}"
            for entry in updated_entries
        )
