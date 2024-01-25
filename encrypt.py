import sys, os
__import__("dotenv").load_dotenv()

try:
    print(''.join(chr(ord(i)+int(os.environ.get("ENC"))) for i in sys.argv[1]))
except:
    print("Usage: python encrypt.py [string]")