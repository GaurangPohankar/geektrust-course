from src.services.courseService import CourseService

class CourseController:
    def __init__(self):
        self.course_service = CourseService()

    def add_course(self, tbl_course, parts):
        return self.course_service.add_course(tbl_course, parts)
