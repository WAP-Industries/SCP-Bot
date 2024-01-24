import sys, os
__import__("dotenv").load_dotenv()

try:
    print(''.join(map(lambda x: chr(ord(x)+int(os.environ.get("ENCRYPT"))), [*sys.argv[1]])))
except Exception as e:
    print(e)
    print("Usage: python encrypt.py [string]") or exit()