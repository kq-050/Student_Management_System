import unittest

from services.student_service import StudentService


class FakeStudentRepository:

    def delete_student(self, roll_no):
        return True

    def search_student(self, roll_no):
        return "Student"

    def sort_students(self, sort_by):
        return ["Student1", "Student2"]

    def get_total_students(self):
        return 20

    def view_students_paginated(self, page, page_size):
        return ["Student1", "Student2"]


class FakeStudentRepositoryFail:

    def delete_student(self, roll_no):
        return False

    def search_student(self, roll_no):
        return None

    def sort_students(self, sort_by):
        return None

    def get_total_students(self):
        return None

    def view_students_paginated(self, page, page_size):
        return None


class TestStudentService(unittest.TestCase):

    def test_delete_student_success(self):
        service = StudentService(FakeStudentRepository())

        result = service.delete_student("22MDSWE")

        self.assertTrue(result)

    def test_delete_student_failure(self):
        service = StudentService(FakeStudentRepositoryFail())

        result = service.delete_student("22MDSWE")

        self.assertFalse(result)

    def test_search_student_not_found(self):
        service = StudentService(FakeStudentRepositoryFail())

        success, message = service.search_student("22MDSWE")

        self.assertFalse(success)

    def test_sort_students(self):
        service = StudentService(FakeStudentRepository())

        success, result = service.sort_students("name")

        self.assertTrue(success)
        self.assertEqual(len(result), 2)

    def test_view_students_paginated(self):
        service = StudentService(FakeStudentRepository())

        success, result = service.view_students_paginated(1)

        self.assertTrue(success)
        self.assertEqual(result["page"], 1)


if __name__ == "__main__":
    unittest.main()
