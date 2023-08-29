class Course:
    def __init__(self, course_offering_id, course_name, instructor, date, min_employee, max_employee, status):
        self.course_offering_id = course_offering_id
        self.course_name = course_name
        self.instructor = instructor
        self.date = date
        self.min_employee = min_employee
        self.max_employee = max_employee
        self.status = status