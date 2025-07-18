from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTableView,
    QPushButton, QMessageBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt
from dialogs import EntryDialog

class Main(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("შტატი მისისიპის პოლიციელების მიერ გაჩერებები")
        self.setGeometry(100, 100, 1350, 700)
        self.db_handler = db
        self.setup_ui()

    def setup_ui(self):
        self.central = QWidget()
        self.layout = QVBoxLayout()

        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")

        self.add_btn.clicked.connect(self.add_record)
        self.update_btn.clicked.connect(self.update_record)
        self.delete_btn.clicked.connect(self.delete_record)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        self.layout.addLayout(btn_layout)

        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

        self.table = "data"
        self.columns = self.db_handler.get_columns(self.table)
        self.load_table(self.table)

    def load_table(self, table_name):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("./dist/data.sqlite3")
        db.open()

        self.model = QSqlTableModel()
        self.model.setTable(table_name)
        self.model.select()
        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)


    def add_record(self):
        dialog = EntryDialog(self.columns, parent=self)
        if dialog.exec_() != dialog.Accepted:
            return
        values = dialog.get_values()
        next_id = self.get_next_raw_row_number()
        full_values = [next_id] + values
        self.db_handler.insert(self.table, full_values)
        self.model.select()

    def get_next_raw_row_number(self):
        query = f"SELECT MAX(raw_row_number) FROM {self.table}"
        self.db_handler.cursor.execute(query)
        result = self.db_handler.cursor.fetchone()[0]
        return (result or 0) + 1

    def update_record(self):
        index = self.table_view.currentIndex()
        row = index.row()
        record = self.model.record(row)
        values = [record.value(col) for col in self.columns]

        dialog = EntryDialog(self.columns, values, mode="Update", parent=self)
        if dialog.exec_() == dialog.Accepted:
            new_values = dialog.get_values()
            row_id = values[0]
            self.db_handler.update(self.table, self.columns, [row_id] + new_values, row_id)
            self.model.select()

    def delete_record(self):
        index = self.table_view.currentIndex()
        row = index.row()
        record = self.model.record(row)
        row_id = record.value(self.columns[0])
        self.db_handler.delete(self.table, self.columns[0], row_id)
        self.model.select()