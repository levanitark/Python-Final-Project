import sys
from PyQt5.QtWidgets import QApplication
from database import Database
from uiview import Main

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database("./dist/data.sqlite3")
    window = Main(db)
    window.show()
    sys.exit(app.exec_())