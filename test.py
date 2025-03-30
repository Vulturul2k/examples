import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit

class CANViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAN Message Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Buton pentru încărcarea unui fișier JSON
        self.load_button = QPushButton("Load JSON")
        self.load_button.clicked.connect(self.load_json)
        layout.addWidget(self.load_button)

        # Câmp de filtrare
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter by Message ID...")
        self.filter_input.textChanged.connect(self.filter_messages)
        layout.addWidget(self.filter_input)

        # Tabel pentru afișarea mesajelor
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Message ID", "Data"])
        layout.addWidget(self.table)

        self.messages = []  # Stocăm mesajele încărcate pentru filtrare

    def load_json(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if not file_name:
            return

        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                self.populate_table(data)
        except Exception as e:
            print("Error loading JSON:", e)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        self.messages = data  # Salvăm mesajele pentru filtrare

        for row, msg in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(msg.get("timestamp", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(msg.get("message_id", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(msg.get("data", ""))))

    def filter_messages(self):
        filter_text = self.filter_input.text()
        self.table.setRowCount(0)  # Ștergem rândurile existente

        filtered_messages = [msg for msg in self.messages if filter_text in str(msg.get("message_id", ""))]
        self.table.setRowCount(len(filtered_messages))

        for row, msg in enumerate(filtered_messages):
            self.table.setItem(row, 0, QTableWidgetItem(str(msg.get("timestamp", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(msg.get("message_id", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(msg.get("data", ""))))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CANViewer()
    viewer.show()
    sys.exit(app.exec_())
