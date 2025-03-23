import sys
import json
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont


class CanJsonProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_packets = [] 
        self.simulator_packets = []  

    def initUI(self):
        self.setWindowTitle('CAN JSON Processor')
        self.setGeometry(100, 100, 900, 400)  

        self.label = QLabel('Introdu JSON-ul CAN:', self)
        self.label.setFont(QFont('Arial', 12))

        self.json_input = QTextEdit(self)
        self.json_input.setFont(QFont('Arial', 10))
        self.json_input.setPlaceholderText("Introdu JSON-ul aici... (poate fi si neformatat)")

        self.process_button = QPushButton('Proceseaza JSON', self)
        self.process_button.setFont(QFont('Arial', 12))
        self.process_button.clicked.connect(self.process_json)

        self.test_button = QPushButton('TEST', self)
        self.test_button.setFont(QFont('Arial', 12))
        self.test_button.clicked.connect(self.testjson)
        
        self.table = QTableWidget()
        self.table.setColumnCount(10) 
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Sursa", "Destinatie", "Nume", "Nivel", "Tip", "Perioada", "Data Size", "Carla Var"
        ])


        self.table.setColumnWidth(0, 60)   # ID
        self.table.setColumnWidth(9, 60)  # Date
        self.table.setColumnWidth(1, 120)  # Sursa
        self.table.setColumnWidth(2, 120)  # Destinatie
        self.table.setColumnWidth(3, 160)  # Nume
        self.table.setColumnWidth(4, 80)   # Nivel
        self.table.setColumnWidth(5, 80)   # Tip
        self.table.setColumnWidth(6, 80)   # Perioada
        self.table.setColumnWidth(7, 80)   # Data Size
        self.table.setColumnWidth(8, 100)  # Carla Var

        	
        self.sim_table = QTableWidget()
        self.sim_table.setColumnCount(10)  
        self.sim_table.setHorizontalHeaderLabels([
            "ID", "Date", "Sursa", "Destinatie", "Nume", "Nivel", "Tip", "Perioada", "Data Size", "Carla Var"
        ])

        self.sim_table.setColumnWidth(0, 60)   # ID
        self.sim_table.setColumnWidth(9, 60)  # Date
        self.sim_table.setColumnWidth(1, 120)  # Sursa
        self.sim_table.setColumnWidth(2, 120)  # Destinatie
        self.sim_table.setColumnWidth(3, 160)  # Nume
        self.sim_table.setColumnWidth(4, 80)   # Nivel
        self.sim_table.setColumnWidth(5, 80)   # Tip
        self.sim_table.setColumnWidth(6, 80)   # Perioada
        self.sim_table.setColumnWidth(7, 80)   # Data Size
        self.sim_table.setColumnWidth(8, 100)  # Carla Var

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.json_input)
        layout.addWidget(self.process_button)
        layout.addWidget(self.test_button)

        # layout.addWidget(self.table)

	
        table_layout = QHBoxLayout()
        table_layout.addWidget(QLabel("📥 Pachete CAN Primite (INPUT)"))
        table_layout.addWidget(QLabel("🚗 Pachete CAN Procesate (SIMULATOR)"))
        
        table_view_layout = QHBoxLayout()
        table_view_layout.addWidget(self.table)
        table_view_layout.addWidget(self.sim_table)
        # layout.addWidget(self.table)
        layout.addLayout(table_layout)
        layout.addLayout(table_view_layout)
        


        self.setLayout(layout)

    def add_packet_to_table(self, packet):
        # table = self.sim_table
        row_position = self.sim_table.rowCount()
        self.sim_table.insertRow(0)

        self.sim_table.setItem(0, 0, QTableWidgetItem(str(packet["can_id"])))
        self.sim_table.setItem(0, 1, QTableWidgetItem(str(packet.get("data", "N/A"))))  
        self.sim_table.setItem(0, 2, QTableWidgetItem(packet.get("src", "N/A")))
        self.sim_table.setItem(0, 3, QTableWidgetItem(packet.get("dst", "N/A")))
        self.sim_table.setItem(0, 4, QTableWidgetItem(packet.get("name", "N/A")))
        self.sim_table.setItem(0, 5, QTableWidgetItem(packet.get("level", "N/A")))
        self.sim_table.setItem(0, 6, QTableWidgetItem(packet.get("type", "N/A")))
        self.sim_table.setItem(0, 7, QTableWidgetItem(str(packet.get("period", "N/A"))))
        self.sim_table.setItem(0, 8, QTableWidgetItem(str(packet.get("datasize", "N/A"))))
        self.sim_table.setItem(0, 9, QTableWidgetItem(packet.get("carlaVar", "N/A")))

        print(f"Pachet CAN afisat in tabel: {packet}")

    def testjson(self):
        print('\n')
        if self.input_packets:
            print(self.input_packets[-1].get("data", "N/A"))

    def process_json(self):
        json_text = self.json_input.toPlainText()

        try:
            json_data = json.loads(json_text)
        except json.JSONDecodeError:
            json_text = self.fix_json(json_text)
            try:
                json_data = json.loads(json_text)
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Eroare", QMessageBox.Ok)
                return


        for can_id, details in json_data.items():
            self.add_command_packet(can_id, details)  
            # row_position = self.table.rowCount()
            self.table.insertRow(0)

            self.table.setItem(0, 0, QTableWidgetItem(str(can_id)))  # ID
            self.table.setItem(0, 1, QTableWidgetItem(str(details.get("data", "N/A")))) # Date
            self.table.setItem(0, 2, QTableWidgetItem(details.get("source", "N/A")))  # Sursa
            self.table.setItem(0, 3, QTableWidgetItem(details.get("execution", "N/A")))  # Destinatie
            self.table.setItem(0, 4, QTableWidgetItem(details.get("name", "N/A")))  # Nume
            self.table.setItem(0, 5, QTableWidgetItem(details.get("level", "N/A")))  # Nivel
            self.table.setItem(0, 6, QTableWidgetItem(details.get("type", "N/A")))  # Tip
            self.table.setItem(0, 7, QTableWidgetItem(str(details.get("period", "N/A"))))  # Perioada
            self.table.setItem(0, 8, QTableWidgetItem(str(details.get("datasize", "N/A"))))  # Data Size
            self.table.setItem(0, 9, QTableWidgetItem(details.get("carlaVar", "N/A")))  # Carla Var

    def add_command_packet(self, can_id, details):

        if details["level"] == "command":
            data_value = details.get("data", None)
            packet = {
                "can_id": can_id,
                "src": details.get("source"),
                "dst": details.get("execution"),
                "name": details.get("name"),
                "level": details.get("level"),
                "type": details.get("type"),
                "period": details.get("period"),
                "datasize": details.get("datasize"),
                "min": details.get("min"),
                "max": details.get("max"),
                "carlaVar": details.get("carlaVar"),
                "data": data_value  
            }
            self.input_packets.append(packet)
            print(f"Command packet added: {packet}")
        else:
            print(f"CAN ID {can_id} is not a command packet.")

    def fix_json(self, text):

        if text.endswith("},}"):
            text = text[:-2]
        if text.endswith("},"):
            text = text[:-1]    

        if not text.startswith("{"):
            text = "{" + text
        if not text.endswith("},}"):
            text = text + "}"

        print(text)
        return text
  