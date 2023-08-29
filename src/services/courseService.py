from src.constants import *
from src.helpers.utility import is_duplicate_item

class CourseService:

    def add_course(self, tbl_course, parts):
        try:
            course_name, instructor, date, minEmployee, maxEmployee = parts[1], parts[2], parts[3], parts[4], parts[5]
            course_offering_id = self.generate_course_offering_id(course_name, instructor)

            if self.is_duplicate_course(tbl_course, course_name, instructor):
                return INPUT_ERROR

            self.add_course_to_table(tbl_course, course_offering_id, course_name, instructor, date, minEmployee, maxEmployee)

            return course_offering_id
        except:
            return INPUT_ERROR

    def generate_course_offering_id(self, course_name, instructor):
        return COURSE_OFFERIN_ID_PREFIX + course_name + "-" + instructor

    def is_duplicate_course(self, tbl_course, course_name, instructor):
        return is_duplicate_item(tbl_course, "course_name", course_name) or is_duplicate_item(tbl_course, "instructor", instructor)

    def add_course_to_table(self, tbl_course, course_offering_id, course_name, instructor, date, minEmployee, maxEmployee):
        tbl_course.append({
            "course_offering_id": course_offering_id,
            "course_name": course_name,
            "instructor": instructor,
            "date": date,
            "minEmployee": minEmployee,
            "maxEmployee": maxEmployee,
            "status": STATUS_ONLINE
        })
