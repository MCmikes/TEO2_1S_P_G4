import sys
import math
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, 
                            QPushButton, QLineEdit, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath



class CalculadoraT(QWidget):
    def __init__(self):
        super().__init__()
        self.configuracion_ui()

    def configuracion_ui(self):

        # configuración de la ventana
        self.setWindowTitle("Calculadora Lab TEO2")
        self.setFixedSize(380, 650)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


        # Frame principal 
        self.frame_principal = QFrame(self)
        self.frame_principal.setGeometry(10, 10, 360, 630)
        self.frame_principal.setStyleSheet("""
            background-color: rgba(40, 40, 40, 230);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)

        layout = QGridLayout(self.frame_principal)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Pantalla donde se muestran los números ingresados 
        self.pantalla = QLineEdit()
        self.pantalla.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.pantalla.setReadOnly(True)
        self.pantalla.setStyleSheet("""
            QLineEdit {
                background-color: rgba(30, 30, 30, 240);
                color: #00ffaa;
                border: 1px solid rgba(0, 255, 170, 0.4);
                border-radius: 12px;
                padding: 15px;
                font-size: 28px;
                font-family: 'Segoe UI';
            }
        """)
        layout.addWidget(self.pantalla, 0, 0, 1, 4)

        # Botones básicos
        botones = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('⌫', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 1, 3), ('☇', 5, 3)
        ]

        # Crear los botones básicos
        self.crear_botones(layout, botones)

        # Botón para poder cerrar la calculadora
        btn_cerrar = QPushButton("✕", self)
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 50, 50, 200);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 80, 80, 230);
            }
        """)
        btn_cerrar.setFixedSize(25, 25)
        btn_cerrar.clicked.connect(self.close)
        btn_cerrar.move(335, 15)


    def crear_botones(self, layout, botones):

        # Estilo base para los botones
        btn_estilo_base =  """
                QPushButton {
                    background-color: rgba(60, 60, 60, 200);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 15px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: rgba(80, 80, 80, 230);
                    border: 1px solid rgba(0, 255, 170, 0.5);
                }
            """
    
        for btn_info in botones:
                texto = btn_info[0]
                btn = QPushButton(texto)
            
                if texto in ['/', '*', '-', '+']:
                    btn.setStyleSheet(btn_estilo_base + """
                        QPushButton {
                            background-color: rgba(255, 150, 0, 220);
                        }
                    """)
                elif texto == '=':
                    btn.setStyleSheet(btn_estilo_base + """
                        QPushButton {
                            background-color: rgba(0, 200, 150, 220);
                            font-size: 24px;
                        }
                    """)
                elif texto == 'C':
                    btn.setStyleSheet(btn_estilo_base + """
                        QPushButton {
                            background-color: rgba(255, 80, 80, 220);
                        }
                    """)
                elif texto == '⌫':
                    btn.setStyleSheet(btn_estilo_base + """
                        QPushButton {
                            background-color: rgba(100, 100, 255, 220);
                        }
                    """)
                elif texto == '☇':
                    btn.setStyleSheet(btn_estilo_base + """
                        QPushButton {
                            background-color: rgba(6, 57, 112, 220);
                        }
                    """)
                else:
                    btn.setStyleSheet(btn_estilo_base)
            
                btn.setFixedSize(60, 60) if texto != '=' else btn.setFixedHeight(60)
            
                if texto == '=':
                    layout.addWidget(btn, *btn_info[1:])
                else:
                    layout.addWidget(btn, *btn_info[1:3])
            
                # Conectar funciones
                if texto == 'C':
                    print("para limpiar la pantalla")
                elif texto == '⌫':
                    print("para eliminar caracter por caracter")
                elif texto == '☇':
                    print("Cambiar a calculadora avanzada")
                elif texto == '=':
                    print("para calcular el resultado")
                elif texto not in ['/', '*', '-', '+']:
                    btn.clicked.connect(lambda _, t=texto: self.pantalla.setText(self.pantalla.text() + t))
   
            
def main():
    app = QApplication(sys.argv)
    app.setStyle('Funsion')
    app.setFont(QFont("Segoe UI", 12))

    calculadora = CalculadoraT()
    calculadora.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()