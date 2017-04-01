import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import QWebView
from PyQt4.QtWebKit import QWebElement
#"The power of the genie is in its confinement"


#this should render the webpage
class WebView(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.newBranch = QtGui.QAction('Branch', self)
        self.newBranch.triggered.connect(self.handleBranch)
	self.table = ParseTable()
	self.navbar = Navigator(self)

    def handleBranch(self):
        branchInfo = self.newBranch.data()
        #print('create new tab:', branchInfo.toString())
	self.table.setTableInfo(self.hit)
	self.travler.findInTree(self.hit.element())

    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()
        self.hit = self.page().currentFrame().hitTestContent(event.pos())
        #print('hit:', hit.imageUrl().toString())
        url = self.hit.linkUrl()
        if url.isValid():
            self.newBranch.setData(self.hit)
            menu.addAction(self.newBranch)
        menu.exec_(event.globalPos())
    def urlHandler(self, url):
	self.load(QUrl(url))
	#TODO:
	#Post load DOM tree parse
	self.travler = DOMTravler(self.page().mainFrame())

class DOMTravler():
    def __init__(self, frame):
	self.setFirst(frame.documentElement())
	print(frame.toHtml().toAscii())
    def findInTree(self, element):
	self.list = [self.first]
	
	#iterate Depth first and fill list
	temp = self.first.firstChild() 
	while ()
	while (not temp.isNull()) and not (temp.__eq__(element)) :
		self.list.append(temp)
		temp = temp.firstChild()

	if(temp.__eq__(element)):
		print('element found!')
		for el in self.list :
			print(el.toInnerXml() + ' : ' + el.toOuterXml() + '\n')
	else:
		print('element not found!')
 
    def setFirst(self, element):
	self.first = element
	


class Navigator(QtGui.QWidget):
    def __init__(self, view):
	super(Navigator, self).__init__()
	self.setUrlHandlerObject(view)
        self.initUI()

    def initUI(self):
	grid = QtGui.QGridLayout()
	self.urlEdit = QtGui.QLineEdit()
	self.goButton = QPushButton("GO!", self)
        self.goButton.clicked.connect(self.goButtonClicked)
	grid.addWidget(self.goButton, 0, 1)
	grid.addWidget(self.urlEdit, 0, 0)
	grid.setSpacing(1)
	self.setLayout(grid)

    def goButtonClicked(self):
	sender = self.sender()
	self.view.urlHandler(self.urlEdit.text())
	#TODO:
	#imput validator
    def setUrlHandlerObject(self, view):
	self.view = view

#this should hold interface form for parseing page selections
class ParseTable(QtGui.QWidget):
    def __init__(self):
	super(ParseTable, self).__init__()
	self.initUI()

    def initUI(self):
	grid = QtGui.QGridLayout()
	self.link = QtGui.QLabel('URL:', self)
	self.image = QtGui.QLabel('Image:', self)
	self.element = QtGui.QLabel('Element:', self)
	self.text = QtGui.QLabel('Text:', self)
	self.title = QtGui.QLabel('Title:', self)
	self.link.setWordWrap(True)
	grid.addWidget(self.link, 1, 0)
	grid.addWidget(self.image, 2, 0)
        grid.addWidget(self.element, 3, 0)
        grid.addWidget(self.text, 4, 0)
        grid.addWidget(self.title, 5, 0)
        #grid.addWidget()
        #grid.addWidget()

	self.setLayout(grid)
#	self.lbl2 = QtGui.QLabel('ImageURL:', self)
#	self.lbl3 = QtGui.QLabel('Element:', self)
    
    def setTableInfo(self, hit):
        self.link.setText(QString(hit.linkUrl().toString()))
        self.image.setText(QString(hit.imageUrl().toString()))
	lister = hit.element().attributeNames()
	classes = hit.element().namespaceUri()
	print(lister.__len__())
	print(classes)
        self.element.setText(classes)
        self.text.setText(hit.linkText())
	self.title.setText(hit.title())
	print(hit.linkUrl().toString())

#TODO:
#Need page middleware for highlighting parse selections
#Need parse Translator for converting selections into regex and/or xpath query
#url field

class VisualParseWindow(QtGui.QWidget):
    def __init__(self):
        super(VisualParseWindow, self).__init__()
        self.initUI()

    def initUI(self):

        grid = QtGui.QGridLayout()
        grid.setSpacing(0)

        view = WebView()
        view.urlHandler('https://www.furaffinity.net/')
	grid.addWidget(view.navbar, 0, 0)
	grid.addWidget(view, 1, 0)
	grid.addWidget(view.table, 1, 1)
	self.setLayout(grid)
        self.setWindowTitle('Test2')
	self.show()
        #view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = VisualParseWindow()
    sys.exit(app.exec_())
