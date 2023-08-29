from src.services.allotService import AllotService

class AllotController:
    def __init__(self):
        self.allot_service = AllotService()

    def allot_course(self, tbl_course, tbl_register, parts):
        return self.allot_service.allot_course(tbl_course, tbl_register, parts)
