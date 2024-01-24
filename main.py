import sys
sys.dont_write_bytecode = True

import os
from bot import *

def main():
    __import__("dotenv").load_dotenv()
    SCPBot.Bot.run(''.join(map(lambda x: chr(ord(x)-int(os.environ.get("ENC"))), [*os.environ.get("TOK")])))


if __name__=="__main__":
    main()