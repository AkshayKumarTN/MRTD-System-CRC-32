from MRTD import validate_mrz_from_json, read_user_data, encode_mrz, write_encoded_records

def main():
    while True:
        print("1. Generate Encoded Passport")  
        print("2. Validate Passport Data")
        option = input("Enter your choice (type 'exit' or 0 to quit): ").strip().lower()
        
        if option == '1':
            file_path = 'records_decoded.json'
            output_file_path = 'records_encoded.json'
            records_encoded = []
            records = read_user_data(file_path)
            for user_record in records['records_decoded']:
                encoded_rocord = encode_mrz(user_record)
                records_encoded.append(encoded_rocord)
            write_encoded_records(records_encoded, output_file_path)
            print("The MRZ encoding process is complete. The encoded records have been saved to 'records_encoded.json'.")
            
        
        elif option == '2':
            file_path = "mrz_input.json"  # Path to the input JSON file
            results = validate_mrz_from_json(file_path)
            
            for result in results:
                print(f"Line 1: {result['line1']}")
                print(f"Line 2: {result['line2']}")
                print(f"Is Valid: {result['is_valid']}")
                print("-" * 40)
        
        elif option == 'exit' or option == '0':
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
