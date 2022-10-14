from doctors_database import Database
from input_output import IO
# from dialoger import Dialoger
def main():
    db = Database() 
    db.get_all_doctors()
    # clf = DrClassifier()
    io = IO()
    # dialoger = Dialoger()
    io.write()
    

if __name__ == '__main__':
    main()
