# from user_model import *
# from ticket_model import *
# from zone_model import *
# MODELS AND PSYCOPG2 CONSIDERATIONS TO SECURELY ACCESS DATABASE:

# Classes are just to organize functions but all functions are @classmethods
# Do not build queries directly into strings without formatting with cursor.execute to avoid xss injection attacks