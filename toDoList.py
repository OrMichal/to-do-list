import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox

class toDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.dataFile = "tasks.json";
        self.setWindowTitle("To-Do List")
        
        self.layout = QVBoxLayout()
        
        self.taskInput = QLineEdit(self)
        self.taskInput.setPlaceholderText("Zadej nový úkol")
        self.layout.addWidget(self.taskInput)
        
        self.addButton = QPushButton("Přidat úkol", self)
        self.addButton.clicked.connect(self.addTask)
        self.layout.addWidget(self.addButton)
        
        self.taskList = QListWidget(self)
        self.layout.addWidget(self.taskList)
        
        self.markDoneButton = QPushButton("Označit jako splněný", self)
        self.markDoneButton.clicked.connect(self.markDone)
        self.layout.addWidget(self.markDoneButton)

        self.changeInput = QLineEdit(self)
        self.changeInput.setPlaceholderText("zde napiš případnou úpravu úkolu")
        self.layout.addWidget(self.changeInput)

        self.changeButton = QPushButton("uložit úpravu označeného úkolu", self)
        self.changeButton.clicked.connect(self.change)
        self.layout.addWidget(self.changeButton)
        
        self.deleteButton = QPushButton("Odstranit úkol", self)
        self.deleteButton.clicked.connect(self.deleteTask)
        self.layout.addWidget(self.deleteButton)
        
        self.setLayout(self.layout)
        self.loadStyles('styl.qss')
        
        self.tasks = []
        self.loadTasksFromFile(self.dataFile)

    def loadTasksFromFile(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                task = line.strip()
                if not task.endswith('(done)'):
                    self.tasks.append(task)
        self.updateTaskList()

    def addTask(self):
        task = self.taskInput.text()
        if task and self.tasks.__contains__(task) == False:
            self.tasks.append(task)
            self.updateTaskList()
            self.saveTaskToFile(task)
            self.taskInput.clear()
        else:
            QMessageBox.warning(self, "Chyba", "Jejda vyskitla se zde chyba při zápisu, nejspíš jsi se pokusil přidat prázdný úkol nebo už ten úkol je v tvém seznamu")

    def saveTaskToFile(self, task):
        with open(self.dataFile, 'a') as file:
            file.write(task + '\n')

    def updateTaskList(self):
        self.taskList.clear()
        self.taskList.addItems(self.tasks)

    def markDone(self):
        selectedTask = self.taskList.currentRow()
        if selectedTask >= 0 and self.tasks[selectedTask].endswith(" (dokončeno)") == False:
            self.tasks[selectedTask] += " (dokončeno)"
            self.updateTaskList()
            self.saveTasksToFile()
        else:
            QMessageBox.warning(self, "Chyba", "Jejda nejspíš jsi vybral k dokončení, už dokončený úkol, můžeš ho smazat nebo jsi nevybral žádný úkol")

    def deleteTask(self):
        selectedTask = self.taskList.currentRow()
        if selectedTask >= 0:
            del self.tasks[selectedTask]
            self.updateTaskList()
            self.saveTasksToFile()
        else:
            QMessageBox.warning(self, "Chyba", "Vyber úkol, který chceš odstranit.")

    def change(self):

        selectedTask = self.taskList.currentRow()
        if selectedTask >= 0 and self.tasks.__contains__(self.changeInput.text()) == False:
            self.tasks[selectedTask] = self.changeInput.text()
            self.updateTaskList()
            self.saveTasksToFile()
            self.changeInput.clear()
        else:
            QMessageBox.warning(self, "Chyba", "nejspíš jsi chtěl upravit úkol na hodnotu, která už je zadána")
    
    def saveTasksToFile(self):
        with open(self.dataFile, 'w') as file:
            for task in self.tasks:
                file.write(task + '\n')
    
    def loadStyles(self, filename):
        try:
            with open(filename, 'r') as file:
                style = file.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print(f"Soubor '{filename}' nebyl nalezen.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = toDoApp()
    window.show()
    sys.exit(app.exec_())




