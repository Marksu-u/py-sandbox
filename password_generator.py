import random
import string

def generate_password(length):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    
    all_characters = letters + digits + symbols
    
    password = ""
    
    for _ in range(length):
        random_char = random.choice(all_characters)
        password += random_char
    return password

if __name__ == "__main__":
    print("Welcome to the Python Password Generator!")
    
    try:
        user_input = input("How long do you want your password to be? ")
        password_length = int(user_input)
        
        new_password = generate_password(password_length)
        print(f"\nYour generated password is: {new_password}")
        
    except ValueError:
        print("Please enter a valid number!")
