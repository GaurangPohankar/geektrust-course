from src.services.cancelService import CancelService

class CancelController:
    def __init__(self):
        self.cancel_service = CancelService()

    def cancel_course(self, tbl_register, parts):
        return self.cancel_service.cancel_course(tbl_register, parts)