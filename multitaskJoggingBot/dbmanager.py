import sqlite3
import os.path

class DBManager:
    cursor: sqlite3.Cursor
    connection: sqlite3.Connection
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_FORMATS = ["gltf", "glb"]#"obj", "fbx"
    SHADER_FORMATS = ["frag", "vert", "comp", "glsl"]

    def __init__(self, dbName : str):
        self.open(dbName)

    def open(self, dbName):
        db_path = os.getcwd() + "\\" + dbName #os.path.join(self.BASE_DIR, dbName) works too
        self.connection = sqlite3.connect(db_path)
        with self.connection:
            self.cursor = self.connection.cursor()

    def insertFile(self, filePath, fileTableName):
        with self.connection:
            with open(filePath, "rb") as input_file:
                self.cursor.execute("INSERT OR IGNORE INTO " + fileTableName +
                                    "(name, file) VALUES(\"" + filePath.split("\\")[-1] + "\", ?)",
                                    [sqlite3.Binary(input_file.read())])
                self.connection.commit()

    def unpackFile(self, intoFile, fileTableName, fileId):
        with self.connection:
            with open(intoFile, "wb") as output_file:
                self.cursor.execute("SELECT file FROM " + fileTableName + " WHERE id = " + str(fileId))
                blob = self.cursor.fetchone()
                output_file.write(blob[0])

    def clear(self, tableName):
        self.cursor.execute('DELETE FROM ' + tableName)
        self.connection.commit()

    def close(self):
        with self.connection:
            self.cursor.close()
            self.connection.close()

    def is_model_format(self, documentName):
        return self.MODEL_FORMATS.__contains__(documentName.split(".")[-1])

    def is_shader_format(self, documentName):
        return self.SHADER_FORMATS.__contains__(documentName.split(".")[-1])