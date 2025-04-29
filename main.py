import sys
import math
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, 
                            QPushButton, QLineEdit, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath



class CalculadoraT(QWidget):
    def __init__(self):
        super().__init__()
        self.modo_avanzado = False
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


        # Botones avanzados
        self.botones_avanzados = [
            ('√', self.raiz_cuadrada),
            ('x^y', self.potencia),
            ('x!', self.factorial),
            ('ln', self.logaritmo)
        ]
        self.config_botones_avanzados(layout)


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
                    btn.clicked.connect(self.borrar_todo)
                elif texto == '⌫':
                    print("para eliminar caracter por caracter")
                    btn.clicked.connect(self.borrar_ultimo)
                elif texto == '☇':
                    btn.clicked.connect(self.cambiar_modo)
                elif texto == '=':
                    btn.clicked.connect(self.calcular_resultados)
                elif texto not in ['/', '*', '-', '+']:
                    btn.clicked.connect(lambda _, t=texto: self.pantalla.setText(self.pantalla.text() + t))
                elif texto not in ['☇']:
                    btn.clicked.connect(lambda _, t=texto: self.pantalla.setText(self.pantalla.text() + t))
   
    
    def config_botones_avanzados(self, layout):
        self.adv_btns = []
        for i, (texto, funcion) in enumerate(self.botones_avanzados):
            btn = QPushButton(texto)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(120, 80, 200, 220);
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(140, 100, 220, 240);
                }
            """)
            btn.setVisible(self.modo_avanzado)
            btn.clicked.connect(funcion)
            layout.addWidget(btn, 6 + i//2, i%2 * 2, 1, 2)
            self.adv_btns.append(btn)
    
    def cambiar_modo(self):
        self.modo_avanzado = not self.modo_avanzado
        for btn in self.adv_btns:
            btn.setVisible(self.modo_avanzado)
        self.setFixedSize(380, 750 if self.modo_avanzado else 650)

    def calcular_resultados(self):
        try:
            expresion = self.pantalla.text()
            resultado = eval(expresion)
            self.pantalla.setText(str(resultado))
        except ZeroDivisionError:
            self.pantalla.setText("Error: División por 0")
        except Exception as e:
            self.pantalla.setText("Error")
    
    def raiz_cuadrada(self):
        print("raiz")
    
    def potencia(self):
        print("potencia")
    
    def factorial(self):
        print("factorial")
    
    def logaritmo(self):
        print("logaritmo")

    # Para mover la calculadora 
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos'):
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            
    def borrar_ultimo(self):
        texto_actual = self.pantalla.text()
        self.pantalla.setText(texto_actual[:-1])
    
    def borrar_todo(self):
        self.pantalla.clear()
    
    
 

            
def main():
    app = QApplication(sys.argv)
    app.setStyle('Funsion')
    app.setFont(QFont("Segoe UI", 12))

    calculadora = CalculadoraT()
    calculadora.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()