# File: main.py
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication , QDialog , QFileDialog
from PySide2.QtCore import QFile

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file = QFile("paomaotoolkit.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    def fileSelect():
        fileName = QFileDialog.getOpenFileNames(window,
                                     "Select one or more files to open",
                                     "C:\\Users\\paomao\\",
                                     "视频 (*.*)")

        #window.filePath.setText("12321312")
        for text in fileName[0]:
            
            window.logsWindow.appendPlainText(text)

        #window.textBrowser.setText(str(fileName[0]))
        print("awdwadawdawdawdwad")
    def normal():
        window.tabWidget.clear()

    window.fileButton.clicked.connect(fileSelect)
    #window.normal.clicked.connect(normal)
    #window.logsWindow.setText("123123")

    ui_file.close()
    window.show()

    sys.exit(app.exec_())