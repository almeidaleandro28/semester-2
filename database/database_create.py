import sqlite3

DATABASE = "LIBRARY.db"

class Connect:
  def __init__(self) -> None:
    self.connection = sqlite3.connect( DATABASE )
    self.cursor = self.connection.cursor()

  def create_tb_user(self) -> None:
    
    self.cursor.execute(
      "CREATE TABLE IF NOT EXISTS TB_BOOK ( \
        BOOK_ID,\
        BOOK_TITLE,\
        BOOK_AUTHOR,\
        BOOK_PUBCOMPANY,\
        BOOK_GENDER,\
        BOOK_AMOUNT )\
      ")
    
  def create_tb_student(self) -> None:

      self.cursor.execute(
      "CREATE TABLE IF NOT EXISTS TB_USER ( \
        USER_ID,\
        USER_NAME,\
        USER_PHONE,\
        USER_ADDRESS,\
        )\
      ")

def create_tb_loan( self ) -> None:
   
   self.cursor.execute(
      "CREATE TABLE IF NOT EXISTS TB_LOAN ( \
        LOAN_ID,\
        LOAN_ID_BOOK,\
        LOAN_ID_USER,\
        LOAN_DAYS,\
        LOAN_DATA_LOAN,\
        LOAN DATA_DEVOLUTION,\
        FOREIGN KEY (LOAN_ID_BOOK) REFERENCES TB_BOOK(BOOK_ID),\
        FOREIGN KEY (LOAN_ID_USER) REFERENCES TB_USER(USER_ID),\
        )\
      ")
