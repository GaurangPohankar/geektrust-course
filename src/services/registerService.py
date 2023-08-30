from src.helpers.utility import get_registration_count, get_course_by_id, is_duplicate_registration, is_course_cancelled
from src.constants import INPUT_ERROR, COURSE_FULL_ERROR, STATUS_PENDING, STATUS_ACCEPTED, COURSE_REGISTRATION_ID_PREFIX

class RegisterService:

    def register_course(self, tbl_course, tbl_register, parts):
        email, course_offering_id = parts[1], parts[2]
        name = self.extract_name_from_email(email)

        if is_duplicate_registration(tbl_register, email, course_offering_id):
            return INPUT_ERROR

        registration_count = get_registration_count(tbl_register, course_offering_id)
        course = get_course_by_id(tbl_course, course_offering_id)
        if not course:
            return INPUT_ERROR

        return self.process_registration(tbl_register, course, name, email, registration_count, course_offering_id)

    def extract_name_from_email(self, email):
        return email.split('@')[0]

    def process_registration(self, tbl_register, course, name, email, registration_count, course_offering_id):
        found_course_name = course['course_name']
        max_course_limit = course['maxEmployee']

        if is_course_cancelled(course):
            return INPUT_ERROR
        elif registration_count >= int(max_course_limit):
            return COURSE_FULL_ERROR
        else:
            course_registration_id = self.generate_course_registration_id(name, found_course_name)

            return self.register_and_return_result(tbl_register, course_registration_id, email, course_offering_id)

    def generate_course_registration_id(self, name, found_course_name):
        return f"{COURSE_REGISTRATION_ID_PREFIX}-{name}-{found_course_name}"

    def register_and_return_result(self, tbl_register, course_registration_id, email, course_offering_id):
        tbl_register.append({
            "course_registration_id": course_registration_id,
            "email": email,
            "course_offering_id": course_offering_id,
            "status": STATUS_PENDING
        })

        return f"{course_registration_id} {STATUS_ACCEPTED}"
