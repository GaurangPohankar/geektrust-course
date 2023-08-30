from src.controllers.courseController import CourseController
from src.controllers.registerController import RegisterController
from src.controllers.allotController import AllotController
from src.controllers.cancelController import CancelController
from src.constants import INPUT_ERROR, ADD_COURSE_COMMAND, REGISTER_COMMAND, ALLOT_COMMAND, CANCEL_COMMAND

class LMSApp:

    def __init__(self):
        self.tbl_course = []
        self.tbl_register = []
        self.course_controller = CourseController()
        self.register_controller = RegisterController()
        self.allot_controller = AllotController()
        self.cancel_controller = CancelController()
        self.command_handlers = {
            (6, ADD_COURSE_COMMAND): self.add_course,
            (3, REGISTER_COMMAND): self.register_course,
            (2, ALLOT_COMMAND): self.allot_course,
            (2, CANCEL_COMMAND): self.cancel_course
        }

    def process_commands(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                self.process_command(line.strip())

    def process_command(self, command):
        if command == "QUIT":
            return

        parts = command.split()
        key = (len(parts), parts[0])

        handler = self.command_handlers.get(key, self.handle_input_error)
        handler(parts)

    def handle_input_error(self, parts):
        print(INPUT_ERROR)

    def add_course(self, parts):
        output = self.course_controller.add_course(self.tbl_course, parts)
        print(output)

    def register_course(self, parts):
        output = self.register_controller.register_course(self.tbl_course, self.tbl_register, parts)
        print(output)

    def allot_course(self, parts):
        output = self.allot_controller.allot_course(self.tbl_course, self.tbl_register, parts)
        print(output)

    def cancel_course(self, parts):
        output = self.cancel_controller.cancel_course(self.tbl_register, parts)
        print(output)
