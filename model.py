from database import conn, select, insert

class Data:
    def __init__(self):
        self.mydb = conn()

    def get_data(self, query, values):
            return select(query, values, self.mydb)
    
    def insert_data(self, query, val):
         return insert(query, val, self.mydb)
    
    # model.py

# Contoh data sebagai variabel
data = "Ini adalah data dari file model.py"

# Atau jika `data` adalah fungsi
def data():
    return "Ini adalah data dari fungsi di file model.py"



        
