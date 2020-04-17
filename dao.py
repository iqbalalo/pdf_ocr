import mysql.connector


class DAO:
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()

    def connect(self):
        try:
            return mysql.connector.connect(
                pool_name="ocr_log",
                pool_size=5,
                host="127.0.0.1",
                port="3306",
                database="ocr_log",
                user="root",
                passwd="1234"
            )
        except Exception as e:
            print(e)
            self.db.close()
            self.db = mysql.connector.connect(pool_name="pdf_ocr")

    def db_close(self):
        try:
            if self.db is not None:
                self.db.close()
            print("DB has been close")
        except Exception as e:
            print(e)

    def create_history(self, lid, parent_id, result):
        sql = "INSERT INTO history VALUES ('{}', '{}', '{}')".format(lid, parent_id, result)

        try:
            self.db = self.connect()
            self.cursor = self.db.cursor()
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.db_close()

    def get_history(self):
        sql = "SELECT * FROM history"

        try:
            self.db = self.connect()
            self.cursor = self.db.cursor()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            records = []
            if rows:
                for i in rows:
                    rec = {"lid": i[0], "parent_id": i[1], "result": i[2]}
                    records.append(rec)

            return records
        except Exception as e:
            print(e)
            return None
        finally:
            self.db_close()