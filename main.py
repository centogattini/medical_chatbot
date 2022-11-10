from doctors_database import Database
from input_output import IO
from classifier import Classifier
from TelegramAPI import TelegramBot
# from dialoger import Dialoger
def main():
    PATH_DATABASE = 'data/database.db'
    BOT_TOKEN = input("please, enter a bot's token:")
    
    db = Database(PATH_DATABASE)
    clf = Classifier(db.get_all_names(), db.get_symps_dict())
    bot = TelegramBot(BOT_TOKEN, clf, db)
    bot.dialog()

if __name__ == '__main__':
    main()
