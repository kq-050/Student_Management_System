import unittest
import validators


class TestValidators(unittest.TestCase):

    def test_valid_roll_number(self):
        is_valid, result = validators.validate_roll_no("22MDSWE")

        self.assertTrue(is_valid)
        self.assertEqual(result, "22MDSWE")

    def test_empty_roll_number(self):
        is_valid, result = validators.validate_roll_no("")

        self.assertFalse(is_valid)

    def test_roll_number_with_spaces(self):
        is_valid, result = validators.validate_roll_no("22 MD SWE")

        self.assertFalse(is_valid)

    # Validate Name
    def test_valid_name(self):
        is_valid, result = validators.validate_name("Lily")

        self.assertTrue(is_valid)
        self.assertEqual(result, "Lily")

    def test_empty_name(self):
        is_valid, result = validators.validate_name(" ")

        self.assertFalse(is_valid)

    def test_name_with_numbers(self):
        is_valid, result = validators.validate_name("Jonr12")

        self.assertFalse(is_valid)

    def test_name_with_special_characters(self):
        is_valid, result = validators.validate_name("Lily@#")

        self.assertFalse(is_valid)

    def test_name_with_leading_and_trailing_spaces(self):
        is_valid, result = validators.validate_name("  john  ")

        self.assertTrue(is_valid)
        self.assertEqual(result, "John")

        # Validate Age tests

    def test_valid_age(self):
        is_valid, result = validators.validate_age(20)

        self.assertTrue(is_valid)
        self.assertEqual(result, 20)

    def test_age_too_young(self):
        is_valid, result = validators.validate_age(17)

        self.assertFalse(is_valid)

    def test_age_too_old(self):
        is_valid, result = validators.validate_age(26)

        self.assertFalse(is_valid)

    def test_negative_age(self):
        is_valid, result = validators.validate_age(-1)

        self.assertFalse(is_valid)

    def test_zero_age(self):
        is_valid, result = validators.validate_age(0)

        self.assertFalse(is_valid)

    # Validate Gender

    def test_valid_gender_male(self):
        is_valid, result = validators.validate_gender("Male")

        self.assertTrue(is_valid)
        self.assertEqual(result, "Male")

    def test_valid_gender_female(self):
        is_valid, result = validators.validate_gender("Female")

        self.assertTrue(is_valid)
        self.assertEqual(result, "Female")

    def test_gender_with_spaces(self):
        is_valid, result = validators.validate_gender("  Male  ")

        self.assertTrue(is_valid)
        self.assertEqual(result, "Male")

    def test_empty_gender(self):
        is_valid, result = validators.validate_gender("")

        self.assertFalse(is_valid)

    # Validate Email

    def test_valid_email(self):
        is_valid, result = validators.validate_email("john@gmail.com")

        self.assertTrue(is_valid)
        self.assertEqual(result, "john@gmail.com")

    def test_email_without_at(self):
        is_valid, result = validators.validate_email("johngmail.com")

        self.assertFalse(is_valid)

    def test_email_without_domain(self):
        is_valid, result = validators.validate_email("john@")

        self.assertFalse(is_valid)

    def test_email_without_username(self):
        is_valid, result = validators.validate_email("@gmail.com")

        self.assertFalse(is_valid)

    def test_empty_email(self):
        is_valid, result = validators.validate_email("")

        self.assertFalse(is_valid)

    # Validate Phone

    def test_valid_phone(self):
        is_valid, result = validators.validate_phone("03123456789")

        self.assertTrue(is_valid)
        self.assertEqual(result, "03123456789")

    def test_phone_too_short(self):
        is_valid, result = validators.validate_phone("03123")

        self.assertFalse(is_valid)

    def test_phone_too_long(self):
        is_valid, result = validators.validate_phone("03123456789123")

        self.assertFalse(is_valid)

    def test_phone_with_letters(self):
        is_valid, result = validators.validate_phone("03123abc789")

        self.assertFalse(is_valid)

    def test_empty_phone(self):
        is_valid, result = validators.validate_phone("")

        self.assertFalse(is_valid)

    def test_roll_number_lowercase(self):
        is_valid, result = validators.validate_roll_no("22mdswe")

        self.assertTrue(is_valid)
        self.assertEqual(result, "22MDSWE")

    def test_roll_number_too_short(self):
        is_valid, result = validators.validate_roll_no("22MD")

        self.assertFalse(is_valid)

    def test_roll_number_with_special_characters(self):
        is_valid, result = validators.validate_roll_no("22MD@WE")

        self.assertFalse(is_valid)
