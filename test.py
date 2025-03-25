from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QTextEdit, QMessageBox, QHBoxLayout, QComboBox,

from PyQt5.QtWidgets import QLineEdit

class CanJsonProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.all_packets = []

    def initUI(self):
        self.setWindowTitle('CAN JSON Processor')
        self.setGeometry(100, 100, 900, 400)

        # Casetă pentru căutare
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Caută în tabel...")
        self.search_box.textChanged.connect(self.filter_table)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Sursa", "Destinatie", "Nume", "Nivel", "Tip"])

        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def process_json(self, json_data):
        self.all_packets.clear()
        self.table.setRowCount(0)

        for can_id, details in json_data.items():
            packet = {
                "can_id": can_id,
                "src": details.get("source", "N/A"),
                "dst": details.get("execution", "N/A"),
                "name": details.get("name", "N/A"),
                "level": details.get("level", "N/A"),
                "type": details.get("type", "N/A"),
            }
            self.all_packets.append(packet)

        self.update_table(self.all_packets)

    def update_table(self, packets):
        self.table.setRowCount(0)
        for packet in packets:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(packet["can_id"])))
            self.table.setItem(row_position, 1, QTableWidgetItem(packet["src"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(packet["dst"]))
            self.table.setItem(row_position, 3, QTableWidgetItem(packet["name"]))
            self.table.setItem(row_position, 4, QTableWidgetItem(packet["level"]))
            self.table.setItem(row_position, 5, QTableWidgetItem(packet["type"]))

    def filter_table(self):
        """Filtrează datele după textul introdus în bara de căutare"""
        search_text = self.search_box.text().lower()
        filtered_packets = [
            p for p in self.all_packets if 
            search_text in p["can_id"].lower() or
            search_text in p["src"].lower() or
            search_text in p["dst"].lower() or
            search_text in p["name"].lower() or
            search_text in p["level"].lower() or
            search_text in p["type"].lower()
        ]
        self.update_table(filtered_packets)
