import unittest

from services.department_service import DepartmentService


class FakeDepartmentRepository:

    def add_department(self, department_name):
        return True

    def view_departments(self):
        return ["Software Engineering", "Computer Science"]


class FakeDepartmentRepositoryFail:

    def add_department(self, department_name):
        return False

    def view_departments(self):
        return []


class TestDepartmentService(unittest.TestCase):

    def test_add_department_success(self):
        service = DepartmentService(FakeDepartmentRepository())

        result = service.add_department("Software Engineering")

        self.assertTrue(result)

    def test_add_department_failure(self):
        service = DepartmentService(FakeDepartmentRepositoryFail())

        result = service.add_department("Software Engineering")

        self.assertFalse(result)

    def test_view_departments(self):
        service = DepartmentService(FakeDepartmentRepository())

        departments = service.view_departments()

        self.assertEqual(len(departments), 2)


if __name__ == "__main__":
    unittest.main()
