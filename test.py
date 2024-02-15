from dotenv import load_dotenv
import os
def test_conn():
    # 
    #if load_dotenv:
        #print("DEBUG: .env file loaded successfully")
    #else:
     #   print("DEBUG: Failed to load .env file")
    # Assuming the .env file is in the same directory as this script
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    #print("DEBUG: Current Working Directory =", os.getcwd())


# ... (rest of your code)otenv