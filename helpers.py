from datetime import datetime
import random

def generate_bill_number():
    year = datetime.now().year
    random_num = random.randint(100, 999)
    return f"PB-{year}-{random_num}"