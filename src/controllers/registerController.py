from src.services.registerService import RegisterService

class RegisterController:
    def __init__(self):
        self.register_service = RegisterService()

    def register_course(self, tbl_course, tbl_register, parts):
        return self.register_service.register_course(tbl_course, tbl_register, parts)
