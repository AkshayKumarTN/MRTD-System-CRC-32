from MRTD import validate_mrz_from_json, read_user_data, encode_mrz

def main():
    while True:
        print("1. Generate Encoded Passport")  
        print("2. Validate Passport Data")
        option = input("Enter your choice (type 'exit' or 0 to quit): ").strip().lower()
        
        if option == '1':
            file_path = 'user_data.json'
            users = read_user_data(file_path)
            for user in users:
                line1, line2 = encode_mrz(user)
                print("Encoded MRZ for user:")
                print("Line 1:", line1)
                print("Line 2:", line2)
                print("-" * 50)
        
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
