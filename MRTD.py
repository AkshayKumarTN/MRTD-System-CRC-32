import json
import zlib
import time
import csv

def load_valid_codes(file_path="valid_codes.json"):
    """Load valid codes from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

VALID_CODES = load_valid_codes()

def calculate_crc32_check_digit(input_data: str) -> int:
    """Calculate a check digit for the input data using CRC32."""
    checksum = zlib.crc32(input_data.encode())
    check_digit = checksum % 10  # Modulus 10 to get the check digit
    return check_digit

def encode_mrz(data):
    """Encode MRZ data based on user input, including calculated CRC32 check digits."""
    # Encode Line 1
    document_type ='p';
    name_field = f"{data['line1']['last_name']}<<{data['line1']['given_name']}".replace(" ", "<").ljust(39, '<')[:39]
    line1 = f"{document_type}<{data['line1']['issuing_country']}{name_field}"
    # Calculate check digits using CRC32 for relevant fields
    passport_check_digit = calculate_crc32_check_digit(data['line2']['passport_number'])
    birth_check_digit = calculate_crc32_check_digit(data['line2']['birth_date'])
    expiry_check_digit = calculate_crc32_check_digit(data['line2']['expiration_date'])
    personal_number_check_digit = calculate_crc32_check_digit(data['line2']['personal_number']) if data['line2']['personal_number'] else '<'
    # Encode Line 2
    passport_number = data['line2']['passport_number'].ljust(9, '<')[:9]
    country_code = data['line2']['country_code'].ljust(3, '<')[:3]
    birth_date = data['line2']['birth_date'].ljust(6, '<')[:6]
    expiration_date = data['line2']['expiration_date'].ljust(6, '<')[:6]
    personal_number = data['line2']['personal_number'].ljust(14, '<')[:14]

    line2 = (f"{passport_number}{passport_check_digit}{country_code}{birth_date}{birth_check_digit}"
             f"{data['line2']['sex']}{expiration_date}{expiry_check_digit}{personal_number}{personal_number_check_digit}")

    return line1+';'+line2

def parse_mrz_line1(line1: str):
    """Parse line 1 of MRZ to extract document type, country, and name fields."""
    document_type = line1[0]
    country = line1[2:5]
    name = line1[5:].replace("<", " ").strip()
    return document_type, country, name

def parse_mrz_line2(line2: str):
    """Parse line 2 of MRZ to extract passport number, date of birth, and expiration date with check digits."""
    passport_number = line2[0:9]
    passport_check_digit = line2[9]
    country = line2[10:13]
    dob = line2[13:19]
    dob_check_digit = line2[19]
    sex = line2[20]
    expiration_date = line2[21:27]
    expiry_check_digit = line2[27]
    personal_number = line2[28:37]
    personal_number_check_digit = line2[-1]
    return passport_number, passport_check_digit, country, dob, dob_check_digit, sex, expiration_date, expiry_check_digit, personal_number, personal_number_check_digit

def validate_code(code: str) -> bool:
    """Validate if a code for country, place of birth, or issuing state is valid."""
    return code in VALID_CODES

def validate_mrz(line1: str, line2: str) -> bool:
      # Check if line2 has the expected length (e.g., 44 characters for a passport MRZ)
    if len(line2) < 43 or len(line2) > 43:  # Adjust the length based on the MRZ standard you're following
        return False
    """Validate the MRZ lines by checking that the check digits are correct."""
    document_type, country_line1, name = parse_mrz_line1(line1)
    # Validate country code in line 1 (issuing state)
    #if not validate_code(country_line1):
        #print(f"Invalid country code in line 1: {country_line1}")
        #return False
    # Parse line 2 fields
    passport_number, passport_check_digit, country_line2, dob, dob_check_digit, sex, expiration_date, expiry_check_digit, personal_number, personal_number_check_digit = parse_mrz_line2(line2)
    #if not validate_code(country_line2):
        #print(f"Invalid country code in line 2: {country_line2}")
        #return False
   # Calculate check digits for each relevant field in line 2
    calculated_passport_check_digit = int(calculate_crc32_check_digit(passport_number))
    calculated_dob_check_digit = calculate_crc32_check_digit(dob)
    calculated_expiry_check_digit = calculate_crc32_check_digit(expiration_date)
    calculated_personal_number_check_digit = calculate_crc32_check_digit(personal_number)
    # Validate all check digits from line 2
    return (
        int(calculated_passport_check_digit) == int(passport_check_digit) and
        int(calculated_dob_check_digit) == int(dob_check_digit) and
        int(calculated_expiry_check_digit) == int(expiry_check_digit) and
        int(calculated_personal_number_check_digit) == int(personal_number_check_digit)
    )

def validate_mrz_from_json(file_path: str):
    """Load MRZ data from a JSON file and validate each MRZ entry."""
    with open(file_path, 'r') as file:
        mrz_data = json.load(file)
    results = []
    for entry in mrz_data['records_encoded']:
        parts = entry.split(';')
        line1 = parts[0]
        line2 = parts[1]
        is_valid = validate_mrz(line1, line2)
        results.append({
            "line1": line1,
            "line2": line2,
            "is_valid": is_valid
        })
    return results

def read_user_data(file_path):
    """Read user data from a JSON file and return as a list of dictionaries."""
    with open(file_path, 'r') as file:
        user_data = json.load(file)
    return user_data

def write_encoded_records(encoded_records, output_path):
    """Writes encoded records to a JSON file."""
    with open(output_path, 'w') as file:
        json.dump({'records_encoded': encoded_records}, file, indent=4)

def measure_execution_times_encode_mrz(input_file, output_csv):
    """Measure execution times for processing records and write results to a CSV."""
    results = []

    # Process for record counts: 100, 1000, ..., 10000
    for k in [100] + list(range(1000, 10001, 1000)):
        # Measure time without tests
        start_no_tests = time.perf_counter()
        records = read_user_data(input_file)['records_decoded'][:k]
        for record in records:
            encode_mrz(record)
        end_no_tests = time.perf_counter()

        # Measure time with tests
        start_with_tests = time.perf_counter()
        for record in records:
            encoded_record = encode_mrz(record)
            assert encoded_record is not None
            assert isinstance(encoded_record, str)
        end_with_tests = time.perf_counter()

        # Calculate execution times
        exec_time_no_tests = end_no_tests - start_no_tests
        exec_time_with_tests = end_with_tests - start_with_tests

        # Append results
        results.append([k, exec_time_no_tests, exec_time_with_tests])
        print(f"Processed {k} records: {exec_time_no_tests:.4f}s (no tests), {exec_time_with_tests:.4f}s (with tests)")
    # Write results to CSV
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Lines_Read", "Exec_Time_No_Tests", "Exec_Time_With_Tests"])
        writer.writerows(results)

    print(f"Execution times have been saved to {output_csv}")

def measure_execution_times_validate_mrz(input_file, output_csv):
    """Measure execution times for validating records and write results to a CSV."""
    results = []

    # Process for record counts: 100, 1000, ..., 10000
    for k in [100] + list(range(1000, 10001, 1000)):
        # Measure time without tests
        start_no_tests = time.perf_counter()
        records = read_user_data(input_file)['records_encoded'][:k]
        for record in records:
            parts = record.split(';')
            line1 = parts[0]
            line2 = parts[1]
            is_valid = validate_mrz(line1, line2)
        end_no_tests = time.perf_counter()

        # Measure time with tests
        start_with_tests = time.perf_counter()
        for record in records:
            parts = record.split(';')
            line1 = parts[0]
            line2 = parts[1]
            is_valid = validate_mrz(line1, line2)
            assert is_valid is not None
            assert isinstance(is_valid, bool)
        end_with_tests = time.perf_counter()

        # Calculate execution times
        exec_time_no_tests = end_no_tests - start_no_tests
        exec_time_with_tests = end_with_tests - start_with_tests

        # Append results
        results.append([k, exec_time_no_tests, exec_time_with_tests])
        print(f"Processed {k} records: {exec_time_no_tests:.4f}s (no tests), {exec_time_with_tests:.4f}s (with tests)")
    # Write results to CSV
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Lines_Read", "Exec_Time_No_Tests", "Exec_Time_With_Tests"])
        writer.writerows(results)

    print(f"Execution times have been saved to {output_csv}")
