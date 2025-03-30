import sys
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CANGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Grafic Viteză și Frână")
        self.setGeometry(100, 100, 800, 500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.start_button = QPushButton("Start Grafic", self)
        self.start_button.clicked.connect(self.start_graph)
        layout.addWidget(self.start_button)
        
        self.data_x = []
        self.data_speed = []
        self.data_brake = []
        self.time_step = 0
        
        self.ani = None

    def update_graph(self, frame):
        self.time_step += 1
        self.data_x.append(self.time_step)
        
        # Simulăm date CAN pentru test
        speed_value = random.randint(0, 120)  # Viteza între 0 și 120 km/h
        brake_value = random.randint(0, 100)  # Frână între 0 și 100%
        
        self.data_speed.append(speed_value)
        self.data_brake.append(brake_value)
        
        if len(self.data_x) > 50:  # Limităm la ultimele 50 de valori
            self.data_x.pop(0)
            self.data_speed.pop(0)
            self.data_brake.pop(0)
        
        self.ax.clear()
        self.ax.plot(self.data_x, self.data_speed, label="Viteză (km/h)", color='blue')
        self.ax.plot(self.data_x, self.data_brake, label="Frână (%)", color='red')
        
        self.ax.set_xlabel("Timp")
        self.ax.set_ylabel("Valoare")
        self.ax.set_title("Grafic Viteză și Frână")
        self.ax.legend()
        self.canvas.draw()
        
    def start_graph(self):
        if self.ani is None:
            self.ani = animation.FuncAnimation(self.figure, self.update_graph, interval=500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CANGraph()
    window.show()
    sys.exit(app.exec_())
