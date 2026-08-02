def validate_name(name):
   name = name.strip()
   
   if not name:
       return False,"Name cannot be Empty!"
   
   if not all(char.isalpha() or char.isspace() for char in name):
       return False, "NName can contain only letters and spaces."
   
   if "  " in name:
       return False, "Name cannot contain multiple consecutive spaces."
   
   #Convert to title case:
   name = " ".join(word.capitalize() for word in name.split())
   
   
   return True,name


def validate_roll_no(roll_no):
    roll_no = roll_no.strip()
    
    
    if not roll_no:
        return False,"Roll no cannot be Empty!"
    
    roll_no = roll_no.upper()
    
    if " " in roll_no:
        return False,"Roll No cannot contain spaces"
    
    if len(roll_no) != 7:
        return False,"Roll No must be 7 characters."
    
    return True,roll_no

def validate_age(age):
    if age < 18:
        return False, "Age must be at least 18."

    if age > 25:
        return False, "Age must not be greater than 25."

    return True, age


def validate_gender(gender):
    # Remove leading and trailing spaces
    gender = gender.strip()

    # Check if empty
    if not gender:
        return False, "Gender cannot be empty."

    # Convert to Title Case
    gender = gender.title()

    # Check valid values
    if gender not in ["Male", "Female", "Other"]:
        return False, "Gender must be Male, Female, or Other."

    return True, gender


def validate_email(email):
    email = email.strip()
    
    if not email:
        return False,"Email cannot be empty."
    
    email = email.lower()
    
    
    if " " in email:
        return False,"Email cannot contain spaces."
    
    if email.count("@") != 1:
        return False,"Email must contain exactly one @"
    
    username, domain = email.split("@")
    
    if not username:
        return False,"Invalid email address."
    
    if "." not in domain:
        return False,"Invalid email address."
    
    return True,email


def validate_phone(phone):
    phone = phone.strip()
    
    if not phone:
        return False,"Phone Number cannot be empty."
    
    if not phone.isdigit():
        return False,"Phone number should contain only digits"
    
    if len(phone) != 11:
        return False,"Phone number should contain 11 digits."
    
    if not phone.startswith("03"):
        return False,"Phone number must start with 03"
    
    return True,phone
    