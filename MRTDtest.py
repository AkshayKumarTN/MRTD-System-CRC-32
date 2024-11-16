import unittest
from MRTD import encode_mrz, validate_mrz, read_user_data, validate_mrz_from_json

class TestMRTD(unittest.TestCase):

    def test_encode_mrz_basic_valid(self):
        """Test that encode_mrz correctly generates MRZ lines for a typical valid input."""
        user_data = {
            "document_type": "P",
            "issuing_country": "UTO",
            "last_name": "DOE",
            "first_name": "JOHN",
            "middle_name": "A",
            "passport_number": "123456789",
            "nationality": "UTO",
            "birth_date": "850101",
            "sex": "M",
            "expiration_date": "300101",
            "personal_number": "1234567890"
        }
        line1, line2 = encode_mrz(user_data)
        self.assertTrue(line1.startswith("P<UTODOE<<JOHN<A"))  # Checking structure of Line 1
        self.assertIn("UTO850101", line2)  # Birth date and nationality in Line 2

    def test_encode_mrz_edge_case_special_characters(self):
        """Test encode_mrz handles names with special characters by removing/ignoring them."""
        user_data = {
            "document_type": "P",
            "issuing_country": "USA",
            "last_name": "O'CONNOR",
            "first_name": "ANNA-MARIA",
            "middle_name": "",
            "passport_number": "987654321",
            "nationality": "USA",
            "birth_date": "920405",
            "sex": "F",
            "expiration_date": "250505",
            "personal_number": ""
        }
        line1, line2 = encode_mrz(user_data)
        self.assertTrue("OCONNOR" not in line1)  # Ensures special characters are handled
        self.assertIn("O'CONNOR", line1)  # Ensures special characters are handled
        self.assertIn("ANNA-MARIA", line1)  # Ensures name is properly encoded
    
    def test_validate_mrz_valid_mrz(self):
        """Test validate_mrz with a valid MRZ input to confirm it returns True."""
        line1 = "P<EUERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C30GBN7408123F1204153ZE184226B8<<<<7"
        self.assertTrue(validate_mrz(line1, line2))  # Valid MRZ should return True
    
    def test_validate_mrz_invalid_check_digit(self):
        """Test validate_mrz with an invalid check digit to ensure it returns False."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "1234567892UTO8501012M30010171234567890<<<<4"  # Incorrect check digit
        self.assertFalse(validate_mrz(line1, line2))  # Invalid MRZ should return False
    
    def test_encode_mrz_missing_data(self):
        """Test encode_mrz handles missing data fields, filling with placeholder characters."""
        user_data = {
            "document_type": "P",
            "issuing_country": "UTO",
            "last_name": "DOE",
            "first_name": "JOHN",
            "middle_name": "",
            "passport_number": "",
            "nationality": "UTO",
            "birth_date": "",
            "sex": "M",
            "expiration_date": "",
            "personal_number": ""
        }
        line1, line2 = encode_mrz(user_data)
        self.assertIn("<<<<", line1)  # Ensures missing data is filled with placeholders
        self.assertIn("<<<<<<<<<<", line2)
    
    def test_validate_mrz_incomplete_mrz(self):
        """Test validate_mrz with incomplete MRZ to confirm it returns False."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "123456789"  # Incomplete second line
        self.assertFalse(validate_mrz(line1, line2))  # Incomplete MRZ should return False

    def test_validate_mrz_invalid_date_format(self):
        """Test validate_mrz with an invalid date format in MRZ to ensure it returns False."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "1234567892UTO0102M30010171234567890<<<<4"  # Invalid birth date format (0102 instead of 850101)
        self.assertFalse(validate_mrz(line1, line2))  # Invalid MRZ should return False
    
    def test_encode_mrz_maximum_length_data(self):
        """Test encode_mrz handles maximum length of data correctly."""
        user_data = {
            "document_type": "P",
            "issuing_country": "UTO",
            "last_name": "A" * 39,  # Max 39 characters
            "first_name": "JOHN",
            "middle_name": "",
            "passport_number": "123456789",
            "nationality": "UTO",
            "birth_date": "850101",
            "sex": "M",
            "expiration_date": "300101",
            "personal_number": "1234567890"
        }
        line1, line2 = encode_mrz(user_data)
        self.assertTrue(len(line1) <= 44)  # Ensure that line 1 is within character limits
        self.assertTrue(len(line2) <= 44)  # Ensure that line 2 is within character limits
    
    def test_validate_mrz_invalid_passport_number(self):
        """Test validate_mrz with an incorrectly formatted passport number."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "123ABC7892UTO8501012M30010171234567890<<<<4"  # Invalid passport number format
        self.assertFalse(validate_mrz(line1, line2))  # Invalid MRZ should return False

    def test_encode_mrz_empty_data(self):
        """Test encode_mrz with empty data to ensure it handles it correctly."""
        user_data = {
            "document_type": "",
            "issuing_country": "",
            "last_name": "",
            "first_name": "",
            "middle_name": "",
            "passport_number": "",
            "nationality": "",
            "birth_date": "",
            "sex": "",
            "expiration_date": "",
            "personal_number": ""
        }
        line1, line2 = encode_mrz(user_data)
        self.assertIn("<<<<", line1)  # Ensure placeholders are used
        self.assertIn("<<<<<<<<<<", line2)
    
    def test_validate_mrz_validate_country_code_Line1(self):
        """Test validate_mrz with an incorrectly formatted country code in Line 1."""
        line1 = "P<UDDDOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "123ABC7892UTO8501012M30010171234567890<<<<4"  # Invalid country code in Line 1
        self.assertFalse(validate_mrz(line1, line2))  # Invalid MRZ should return False
    
    def test_validate_mrz_validate_country_code_Line2(self):
        """Test validate_mrz with an incorrectly formatted country code in Line 1."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "123ABC7892UWW8501012M30010171234567890<<<<4"  # Invalid country code in Line 2
        self.assertFalse(validate_mrz(line1, line2))  # Invalid MRZ should return False

    def test_read_user_data(self):
        """Test read_user_data"""
        file_path = 'user_data.json'
        result = read_user_data(file_path)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["first_name"], "JOHN")
        self.assertEqual(result[1]["last_name"], "SMITH")
        self.assertEqual(result[1]["passport_number"], "987654321")

    def test_validate_mrz_from_json(self):
       
        file_path = "mrz_input.json"
        # Call the function to validate MRZ from JSON data
        result = validate_mrz_from_json(file_path)

        # Verify the results
        self.assertEqual(len(result), 3)
        self.assertTrue(result[0]["is_valid"])
        self.assertTrue(result[1]["is_valid"])

    # Mutation Test Cases
    def test_validate_mrz_exceed_length_42(self):
        """Test validate_mrz for an MRZ line2 with exceeding 42 characters."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C30GBN7408123F1204153ZE184226B8<<<<<<<7" 
        self.assertFalse(validate_mrz(line1, line2))

    def test_validate_mrz_short_length_42(self):
        """Test validate_mrz for an MRZ line2 with length shorter than 42 characters."""
        line1 = "P<UTODOE<<JOHN<A<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C30GBN7408123F1204153ZE18422<<7" 
        self.assertFalse(validate_mrz(line1, line2))

