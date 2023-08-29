import unittest
from io import StringIO
from unittest.mock import patch
import geektrust  # Assuming your script is named geektrust.py
from src.controllers.courseController import CourseController
from src.controllers.registerController import RegisterController
from src.controllers.allotController import AllotController
from src.controllers.cancelController import CancelController
from src.services.courseService import CourseService
from src.services.registerService import RegisterService

class TestLMSFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def setUp(self):
        self.tbl_course = []
        self.tbl_register = []

        # Instantiate the controller classes with the service instances
        self.course_controller = CourseController()
        self.register_controller = RegisterController()
        self.allot_controller = AllotController()
        self.cancel_controller = CancelController()


    def test_add_course_missing_parameters(self):
        parts = ["ADD-COURSE-OFFERING"]  # Missing parameters
        output = self.course_controller.add_course(self.tbl_course, parts)
        self.assertEqual(output, "INPUT_DATA_ERROR")
        self.assertEqual(len(self.tbl_course), 0)  # Ensure that the course wasn't added


    def test_add_course_offering(self):
        parts = ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231015", "1", "5"]
        output = self.course_controller.add_course(self.tbl_course, parts)
        self.assertEqual(output, "OFFERING-DATASCIENCE-ALICE")
        self.assertEqual(len(self.tbl_course), 1)

    def test_duplicate_course_name(self):
        parts1 = ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231015", "1", "5"]
        parts2 = ["ADD-COURSE-OFFERING", "DATASCIENCE", "BOB", "20231020", "2", "6"]
        self.course_controller.add_course(self.tbl_course, parts1)
        output = self.course_controller.add_course(self.tbl_course, parts2)
        self.assertEqual(output, "INPUT_DATA_ERROR")

    def test_duplicate_instructor_name(self):
        parts1 = ["ADD-COURSE-OFFERING", "DATAANALYSIS", "ALICE", "20231015", "1", "5"]
        parts2 = ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231020", "2", "6"]
        self.course_controller.add_course(self.tbl_course, parts1)
        output = self.course_controller.add_course(self.tbl_course, parts2)
        self.assertEqual(output, "INPUT_DATA_ERROR")

    def test_register_course(self):
        self.course_controller.add_course(self.tbl_course, ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231015", "1", "5"])
        parts = ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"]
        output = self.register_controller.register_course(self.tbl_course, self.tbl_register, parts)
        self.assertEqual(output, "REG-COURSE-ALICE-DATASCIENCE ACCEPTED")

    def test_register_course_full_error(self):
        self.course_controller.add_course(self.tbl_course, ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231015", "1", "1"])
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        parts = ["REGISTER", "BOB@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"]
        output = self.register_controller.register_course(self.tbl_course, self.tbl_register, parts)
        self.assertEqual(output, "COURSE_FULL_ERROR")


    def test_allot_course(self):
        self.course_controller.add_course(self.tbl_course, ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231015", "2", "5"])
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "BOB@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        parts = ["ALLOT", "OFFERING-DATASCIENCE-ALICE"]
        output = self.allot_controller.allot_course(self.tbl_course, self.tbl_register, parts)
        expected_output = (
            "REG-COURSE-ALICE-DATASCIENCE ALICE@GMAIL.COM OFFERING-DATASCIENCE-ALICE DATASCIENCE ALICE 20231015 CONFIRMED\n"
            "REG-COURSE-BOB-DATASCIENCE BOB@GMAIL.COM OFFERING-DATASCIENCE-ALICE DATASCIENCE ALICE 20231015 CONFIRMED"
        )
        self.assertEqual(output, expected_output)

    def test_cancel_course(self):
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        parts = ["CANCEL", "REG-COURSE-ALICE-DATASCIENCE"]
        output = self.cancel_controller.cancel_course(self.tbl_register, parts)
        self.assertEqual(output, "REG-COURSE-ALICE-DATASCIENCE CANCEL_REJECTED")


    def test_cancel_course_not_found(self):
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        parts = ["CANCEL", "UNKNOWN-COURSE-ID"]
        output = self.cancel_controller.cancel_course(self.tbl_register, parts)
        self.assertEqual(output, "UNKNOWN-COURSE-ID CANCEL_REJECTED")

    def test_cancel_course_already_confirmed(self):
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        parts = ["ALLOT", "OFFERING-DATASCIENCE-ALICE"]
        self.allot_controller.allot_course(self.tbl_course, self.tbl_register, parts)
        parts = ["CANCEL", "REG-COURSE-ALICE-DATASCIENCE"]
        output = self.cancel_controller.cancel_course(self.tbl_register, parts)
        self.assertEqual(output, "REG-COURSE-ALICE-DATASCIENCE CANCEL_REJECTED")


    def test_register_course_duplicate_registration(self):
        self.course_controller.add_course(self.tbl_course, ["ADD-COURSE-OFFERING", "DATASCIENCE", "ALICE", "20231015", "1", "5"])
        self.register_controller.register_course(self.tbl_course, self.tbl_register, ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"])
        parts = ["REGISTER", "ALICE@GMAIL.COM", "OFFERING-DATASCIENCE-ALICE"]
        output = self.register_controller.register_course(self.tbl_course, self.tbl_register, parts)
        self.assertEqual(output, "INPUT_DATA_ERROR")


if __name__ == "__main__":
    unittest.main()
