__import__("sys").dont_write_bytecode = True

import os
from bot import *

def main():
    __import__("dotenv").load_dotenv()
    BRBot.LoadStats()
    BRBot.Bot.run(''.join(chr(ord(i)-int(os.environ.get("ENC"))) for i in os.environ.get("TOK")))


if __name__=="__main__":
    main()