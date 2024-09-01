import unittest
from unittest.mock import patch
from MainCode2 import register_student, is_valid_email, is_valid_date_of_birth, generate_student_id, encrypt_data

class TestBootcampManagementSystem(unittest.TestCase):

    # Test the is_valid_email function
    def test_is_valid_email_valid(self):
        self.assertTrue(is_valid_email("test@example.com"))

    def test_is_valid_email_invalid(self):
        self.assertFalse(is_valid_email("invalid-email"))

    # Test the is_valid_date_of_birth function
    def test_is_valid_date_of_birth_valid(self):
        self.assertTrue(is_valid_date_of_birth("2000-01-01"))

    def test_is_valid_date_of_birth_future_date(self):
        self.assertFalse(is_valid_date_of_birth("3000-01-01"))

    def test_is_valid_date_of_birth_old_date(self):
        self.assertFalse(is_valid_date_of_birth("1800-01-01"))

    def test_is_valid_date_of_birth_invalid_format(self):
        self.assertFalse(is_valid_date_of_birth("01-01-2000"))

    # Test the generate_student_id function
    def test_generate_student_id(self):
        student_id = generate_student_id("Doe")
        self.assertTrue(student_id.startswith("Doe-"))
        self.assertEqual(len(student_id.split('-')[-1]), 4)

    # Test the encrypt_data function
    def test_encrypt_data(self):
        data = {"studentID": "1234", "name": "John Doe"}
        encrypted_data = encrypt_data(data)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(data, encrypted_data)  # Ensure data is encrypted

    # Test the register_student function with mocks
    @patch('MainCode2.is_valid_email')
    @patch('MainCode2.is_valid_date_of_birth')
    @patch('MainCode2.generate_student_id')
    @patch('MainCode2.encrypt_data')
    def test_successful_registration(self, mock_encrypt, mock_generate_id, mock_valid_dob, mock_valid_email):
        mock_valid_email.return_value = True
        mock_valid_dob.return_value = True
        mock_generate_id.return_value = "Doe-1234"
        mock_encrypt.return_value = {"encrypted": "data"}

        with patch('builtins.print') as mock_print:
            register_student()

        mock_print.assert_any_call("Registration successful! ID: Doe-1234")
        mock_encrypt.assert_called_once()

    @patch('MainCode2.is_valid_email')
    def test_invalid_email_registration(self, mock_valid_email):
        mock_valid_email.return_value = False

        with patch('builtins.print') as mock_print:
            register_student()

        mock_print.assert_any_call("An error occurred during registration: Invalid email format.")

    @patch('MainCode2.is_valid_email')
    @patch('MainCode2.is_valid_date_of_birth')
    def test_invalid_dob_registration(self, mock_valid_dob, mock_valid_email):
        mock_valid_email.return_value = True
        mock_valid_dob.return_value = False

        with patch('builtins.print') as mock_print:
            register_student()

        mock_print.assert_any_call("An error occurred during registration: Invalid date of birth.")

if __name__ == '__main__':
    unittest.main()
