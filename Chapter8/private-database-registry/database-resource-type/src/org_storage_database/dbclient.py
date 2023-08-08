import pymysql

class DbClient():
    CREATE_DB = "CREATE DATABASE {};"
    CREATE_USER = "CREATE USER '{}'@'%' IDENTIFIED BY '{}';"
    GRANT = "GRANT ALL PRIVILEGES ON {}.* TO '{}'@'%';"
    FLUSH = "FLUSH PRIVILEGES;"
    DELETE_DB = "DROP DATABASE {}"
    DELETE_USER = "DROP USER '{}'"
    DB_EXISTS = "SHOW DATABASES LIKE '{}'"
    USER_EXISTS = "SELECT user FROM mysql.user where user='{}'"
    CHANGE_USER_PASSWORD = "ALTER USER '{}'@'%' IDENTIFIED BY '{}'"
    
    def __init__(self, endpoint, user, password):
        self.connection = pymysql.connect(host=endpoint,
                                          user=user,
                                          password=password
                                          )
        self.cursor = self.connection.cursor()
           
    def db_exists(self, db):
        if self.cursor.execute(self.DB_EXISTS.format(db)):
            return True
 
    def user_exists(self, user):
        if self.cursor.execute(self.USER_EXISTS.format(user)):
            return True
    
    def delete_db(self, db):
        self.cursor.execute(self.DELETE_DB.format(db))
    
    def delete_user(self, user):
        self.cursor.execute(self.DELETE_USER.format(user))
            
    def delete(self, db, user):
        if self.db_exists(db):
            self.delete_db(db)
        
        if self.user_exists(user):
            self.delete_user(user)
    
    def create_or_update(self, db, user, pw):
        if self.db_exists(db):
            self.delete_db(db)
        
        if self.user_exists(user):
            self.delete_user(user)
        
        self.cursor.execute(self.CREATE_USER.format(user,pw))
        self.cursor.execute(self.CREATE_DB.format(db))
        self.cursor.execute(self.GRANT.format(db, user))
        self.cursor.execute(self.FLUSH)

    def change_user_password(self, user, pw):
        if not self.user_exists(user):
            raise ValueError(f'User {user} does not exist!')
            
        self.cursor.execute(self.CHANGE_USER_PASSWORD.format(user, pw))
