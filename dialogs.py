from PyQt5.QtWidgets import (
    QLineEdit, QLabel, QFormLayout, QDialog, QDialogButtonBox, QComboBox, QDateEdit
)
from PyQt5.QtCore import QDate, Qt

class EntryDialog(QDialog):
    def __init__(self, columns, values=None, mode="Add", parent=None):

        self.counties_in_mississippi = [
            "Alcorn County",
            "Calhoun County",
            "Chickasaw County",
            "Clay County",
            "Covington County",
            "DeSoto County",
            "Forrest County",
            "Franklin County",
            "George County",
            "Grenada County",
            "Harrison County",
            "Hinds County",
            "Holmes County",
            "Issaquena County",
            "Itawamba County",
            "Jackson County",
            "Jones County",
            "Lafayette County",
            "Leake County",
            "Lee County",
            "Leflore County",
            "Lincoln County",
            "Lowndes County",
            "Madison County",
            "Marshall County",
            "NA",
            "Oktibbeha County",
            "Pearl River County",
            "Pike County",
            "Pontotoc County",
            "Rankin County",
            "Simpson County",
            "Smith County",
            "Stone County",
            "Sunflower County",
            "Tate County",
            "Union County",
            "Warren County",
            "Washington County",
            "Yalobusha County"
        ]

        self.departments = {
            "9": "Chickasaw County Sheriff Office",
            "19": "Franklin County Sheriff Office",
            "20": "George County Sheriff Office",
            "26": "Holmes County Sheriff Office",
            "29": "Itawamba County Sheriff Office",
            "30": "Jackson County Sheriff Office",
            "36": "Lafayette County Sheriff Office",
            "44": "Lowndes County Sheriff Office",
            "55": "Pearl River County Sheriff Office",
            "61": "Rankin County Sheriff Office",
            "66": "Stone County Sheriff Office",
            "67": "Sunflower County Sheriff Office",
            "201": "Corinth Police Dept",
            "1301": "West Point Police Dept",
            "1701": "Hernando Police Dept",
            "1702": "Olive Branch Police Dept",
            "1703": "Southaven Police Dept",
            "1704": "Horn Lake Police Dept",
            "1801": "Hattiesburg Police Dept",
            "2201": "Grenada Police Dept",
            "2401": "Biloxi Police Dept",
            "2403": "Gulfport Police Dept",
            "2504": "Jackson Police Dept",
            "2506": "Raymond Police Dept",
            "2604": "Lexington Police Dept",
            "3005": "Pascagoula Police Dept",
            "3401": "Ellisville Police Dept",
            "3601": "Oxford Police Dept",
            "4001": "Carthage Police Dept",
            "4107": "Tupelo Police Dept",
            "4301": "Brookhaven Police Dept",
            "4403": "Columbus Police Dept",
            "4504": "Ridgeland Police Dept",
            "4702": "Holly Springs Police Dept",
            "5302": "Starkville Police Dept",
            "5702": "McComb Police Dept",
            "5802": "Pontotoc Police Dept",
            "6103": "Flowood Police Dept",
            "6104": "Pearl Police Dept",
            "6106": "Richland Police Dept",
            "6504": "Taylorsville Police Dept",
            "6601": "Wiggins Police Dept",
            "6902": "Senatobia Police Dept",
            "7303": "New Albany Police Dept",
            "7501": "Vickburg Police Dept",
            "8104": "Water Valley Police Dept",
            "9076": "Mississippi Highway Patrol",
            "9163": "Ms Dept of Transportation"
        }

        self.violations = [
            'B08', 'B26', 'B30', 'B51', 'B53', 'B55', 'D36', 'E01',
            'F02', 'F04', 'M14', 'M34', 'M81', 'N01', 'S92', 'S93', 'T01'
        ]

        self.race_map = {"black": "b", "white": "w", "asian": "a"}

        self.sexes = ["male", "female"]

        super().__init__(parent)
        if mode == "Add":
            self.setWindowTitle("ჩანაწერის დამატება")
        else:
            self.setWindowTitle("ჩანაწერის განახლება")
        self.inputs = {}
        layout = QFormLayout(self)

        for col, val in zip(columns, values if values else [None] * len(columns)):
            if col == "raw_row_number":
                continue

            if col == "subject_sex":
                field = QComboBox()
                field.addItems(self.sexes)
                if val:
                    index = field.findText(val, Qt.MatchFixedString)
                    if index >= 0:
                        field.setCurrentIndex(index)

            elif col == "county_name":
                field = QComboBox()
                field.addItems(self.counties_in_mississippi)
                if val:
                    index = field.findText(val, Qt.MatchFixedString)
                    if index >= 0:
                        field.setCurrentIndex(index)

            elif col == "department_id":
                field = QComboBox()
                field.addItems(self.departments.keys())
                field.currentTextChanged.connect(lambda dept_id, f=field: self.sync_department_name(dept_id))

            elif col == "department_name":
                field = QComboBox()
                field.addItems(self.departments.values())
                field.currentTextChanged.connect(lambda name, f=field: self.sync_department_id(name))
                if val:
                    index = field.findText(val, Qt.MatchFixedString)
                    if index >= 0:
                        field.setCurrentIndex(index)

            elif col == "violation":
                field = QComboBox()
                field.addItems(self.violations)
                field.currentTextChanged.connect(self.toggle_speed_fields)
                if val:
                    index = field.findText(val, Qt.MatchFixedString)
                    if index >= 0:
                        field.setCurrentIndex(index)

            elif col in ["speed", "posted_speed"]:
                field = QLineEdit()
                field.setDisabled(True)
                if val:
                    field.setText(val)
                else:
                    field.setText("NA")

            elif col == "date":
                field = QDateEdit()
                field.setCalendarPopup(True)
                field.setDisplayFormat("MM/dd/yyyy")
                if val:
                    field.setDate(QDate.fromString(val, "MM/dd/yyyy"))
                else:
                    field.setDate(QDate.currentDate())

            else:
                field = QLineEdit()
                if val:
                    field.setText(str(val))

            layout.addRow(QLabel(col), field)
            self.inputs[col] = field


        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def sync_department_name(self, dept_id):
        dept_name = self.departments.get(dept_id)
        if dept_name:
            name_combo = self.inputs.get("department_name")
            if name_combo:
                index = name_combo.findText(dept_name)
                if index >= 0:
                    name_combo.setCurrentIndex(index)

    def sync_department_id(self, dept_name):
        for dept_id, name in self.departments.items():
            if name == dept_name:
                id_combo = self.inputs.get("department_id")
                if id_combo:
                    index = id_combo.findText(dept_id)
                    if index >= 0:
                        id_combo.setCurrentIndex(index)

    def toggle_speed_fields(self, violation_code):
        enable = violation_code == "S92"
        for key in ["speed", "posted_speed"]:
            field = self.inputs.get(key)
            if field:
                field.setDisabled(not enable)
                if not enable:
                    field.setText("NA")
                else:
                    field.setText("")

    def get_values(self):
        values = []
        for widget in self.inputs.values():
            if isinstance(widget, QComboBox):
                values.append(widget.currentText())
            elif isinstance(widget, QDateEdit):
                values.append(widget.date().toString("MM/dd/yyyy"))
            else:
                values.append(widget.text())
        return values


