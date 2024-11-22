from MRTD import validate_mrz_from_json, read_user_data, encode_mrz, write_encoded_records, measure_execution_times
import time


def main():
    while True:
        print("1. Generate Encoded Passport")  
        print("2. Validate Passport Data")
        print("3. Measure Execution Times")
        option = input("Enter your choice (type 'exit' or 0 to quit): ").strip().lower()
        
        if option == '1':
            file_path = 'records_decoded.json'
            output_file_path = 'records_encoded.json'
            records_encoded = []
            records = read_user_data(file_path)
            start_time = time.perf_counter()
            for user_record in records['records_decoded']:
                encoded_rocord = encode_mrz(user_record)
                records_encoded.append(encoded_rocord)
            end_time = time.perf_counter()
            write_encoded_records(records_encoded, output_file_path)
            print("The MRZ encoding process is complete. The encoded records have been saved to 'records_encoded.json'.")
            print(f"Downloaded the tutorial in {end_time - start_time:0.4f} seconds")
            
        
        elif option == '2':
            file_path = "records_encoded.json"  # Path to the input JSON file
            results = validate_mrz_from_json(file_path)
            is_valid_true = 0
            is_valid_false = 0
            for result in results:
                if result['is_valid'] == True:
                    is_valid_true +=1
                else:
                    is_valid_false +=1
                    print(f"Line 1: {result['line1']}")
                    print(f"Line 2: {result['line2']}")
                    print(f"Is Valid: {result['is_valid']}")
                    print("-" * 40)
            print('Total Valid Data : ', is_valid_true)
            print('Total Invalid Data : ', is_valid_false)
            
        elif option == '3':
            input_file = 'records_decoded.json'
            output_csv = 'execution_times.csv'
            measure_execution_times(input_file, output_csv)
        
        elif option == 'exit' or option == '0':
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
