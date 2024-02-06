__import__("sys").dont_write_bytecode = True

from bot import *

def main():
    __import__("dotenv").load_dotenv()
    BRBot.LoadStats()
    BRBot.Bot.run(''.join(chr(ord(i)-int(environ.get("ENC"))) for i in environ.get("TOK")))


if __name__=="__main__":
    main()