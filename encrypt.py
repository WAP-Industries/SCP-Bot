import sys, os
__import__("dotenv").load_dotenv()

try:
    print(''.join(map(lambda x: chr(ord(x)+int(os.environ.get("ENC"))), [*sys.argv[1]])))
except:
    print("Usage: python encrypt.py [string]")