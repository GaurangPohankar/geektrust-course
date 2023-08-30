from src.constants import *
from datetime import datetime


# def is_course_cancelled(course):
#     return course and course['status'] == STATUS_CANCELLED





class CancelUtility:
    @staticmethod
    def cal_is_registration_cancelled(tbl_register, course_registration_id):
        for registration in tbl_register:
            if registration['course_registration_id'] == course_registration_id and registration['status'] != 'CONFIRMED':
                return True
        return False

    @staticmethod
    def cal_update_status(tbl_register, course_registration_id, status):
        updated_register = []
        for registration in tbl_register:
            if registration['course_registration_id'] == course_registration_id:
                registration['status'] = status
            updated_register.append(registration)
        return updated_register


class CourseUtility:
    @staticmethod
    def is_duplicate_item(item_list, key, value):
        for item in item_list:
            if item[key] == value:
                return True
        return False


class RegistrationUtility:
    @staticmethod
    def get_course_by_id(tbl_course, course_offering_id):
        for course in tbl_course:
                if course['course_offering_id'] == course_offering_id:
                    return course
        return None
    
    @staticmethod
    def get_registration_count(tbl_register, course_offering_id):
        count = 0
        for registration in tbl_register:
            if registration['course_offering_id'] == course_offering_id:
                if registration['status'] == 'PENDING' or registration['status'] == 'CONFIRMED':
                    count += 1
        return count

    @staticmethod
    def is_duplicate_registration(registrations, email, course_offering_id):
        for registration in registrations:
            if registration["email"] == email and registration["course_offering_id"] == course_offering_id:
                return True
        return False
    
    @staticmethod
    def is_course_cancelled(course):
        return course and course['status'] == STATUS_CANCELLED
    

class AllotmentUtility:
    
    @staticmethod
    def find_course_by_id(tbl_course, course_offering_id):
        for course in tbl_course:
            if course['course_offering_id'] == course_offering_id:
                return course
        return None
    
    @staticmethod
    def get_current_date():
        return datetime.now().strftime('%d%m%Y')

    @staticmethod
    def allot_is_course_cancelled(course, current_date, registration_count, min_course_limit):
        return int(current_date) > int(course['date']) and registration_count < int(min_course_limit)

    @staticmethod
    def update_statuses(tbl_register, course_offering_id, course_status):
        updated_entries = []
        for registration in tbl_register:
            if registration['course_offering_id'] == course_offering_id and registration['status'] == STATUS_PENDING:
                if course_status == STATUS_CANCELLED:
                    registration['status'] = STATUS_COURSE_CANCELED
                else:
                    registration['status'] = STATUS_CONFIRMED
                updated_entries.append(registration)
        return updated_entries

