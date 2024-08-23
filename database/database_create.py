import sqlite3

DATABASE = "LIBRARY.db"

class Connect:
  def __init__(self) -> None:
    self.connection = sqlite3.connect( DATABASE )
    self.cursor = self.connection.cursor()

  def create_tb_user(self) -> None:
    
    self.cursor.execute()
