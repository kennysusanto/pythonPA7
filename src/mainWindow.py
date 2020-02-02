from Tkinter import *
from dataStructs import *
from tkcolorpicker import *


class mainWindow:
    def __init__(self, master):
        self.master = master
        master.title("testPolygon")
        master.geometry("+300+100")
        self.width = 640
        self.height = 480

        self.framell = Frame(self.master)
        self.framell.pack(side="left", fill="y")

        self.frameleft = Frame(self.master)
        self.frameleft.pack(side="left", fill="y")

        self.framelt = Frame(self.frameleft)
        self.framelt.pack(side="top", fill="both")

        self.framelb = Frame(self.frameleft)
        self.framelb.pack(side="bottom", fill="both")

        self.btn_pointer = Button(self.framelt, text="Pointer", command=self.pointer)
        self.btn_pointer.grid(column=0, row=0, sticky=W + E)

        self.btn_poly = Button(self.framelt, text="New Polygon", command=self.polyInit)
        self.btn_poly.grid(column=0, row=1, sticky=W + E)

        self.btn_poli = Button(self.framelt, text="New Polyline")
        self.btn_poli.grid(column=0, row=2, sticky=W + E)
        self.btn_poli.config(state=DISABLED)

        self.btn_color = Button(self.framelt, text="Change Color", command=self.changeColor)
        self.btn_color.grid(column=0, row=3, sticky=W + E)

        self.btn_add = Button(self.framelt, text="Add Node", command=self.addWindow)
        self.btn_add.grid(column=0, row=4, sticky=W + E)

        self.btn_del = Button(self.framelt, text="Delete Node", command=self.delWindow)
        self.btn_del.grid(column=0, row=5, sticky=W + E)

        self.btn_delo = Button(self.framelt, text="Delete Object", command=self.deleteObj)
        self.btn_delo.grid(column=0, row=6, sticky=W + E)
        self.btn_delo.config(state=DISABLED)

        self.btn_clear = Button(self.framelt, text="Clear", command=self.clear)
        self.btn_clear.grid(column=0, row=7, sticky=W + E)

        self.btn_close = Button(self.framelb, text="Close", command=master.quit)
        self.btn_close.pack(side="bottom", fill="x")

        self.frameright = Frame(self.master)
        self.frameright.pack(side="right", fill="x")

        self.plistbox = Listbox(self.framell, selectmode=SINGLE)
        self.plistbox.pack(side="top", fill="both")
        self.plistbox.bind('<<ListboxSelect>>', self.changeSelectedp)
        self.lbl1 = Label(self.framell, text="Polygon").pack(side="top", fill="both")

        self.nlistbox = Listbox(self.framell)
        self.nlistbox.pack(side="bottom", fill="both")
        self.lbl2 = Label(self.framell, text="Polygon Nodes").pack(side="bottom", fill="both")
        self.nlistbox.bindtags((self.nlistbox, self.framell, "all"))

        self.lbl_text_mousepos = StringVar()
        self.lbl_text_mousepos.set("mousepos")
        self.lbl_mouse = Label(self.framelb, textvariable=self.lbl_text_mousepos)
        self.lbl_mouse.pack(side="bottom", fill="x")

        self.btn_pointer.config(state=DISABLED)
        self.btn_add.config(state=DISABLED)
        self.btn_color.config(state=DISABLED)
        self.btn_del.config(state=DISABLED)
        self.create()
        self.o = Point(0, 0)
        self.polylist = Polylist()
        # self.polyArr = []
        self.arrCounter = -1
        self.current = None
        self.selectedP = 0  # passing selected polygon (int)
        self.selectedN = None  # passing selected node (int)
        self.selectedNobj = None  # passing selected node (object)
        self.rectslist = []  # list of polygon rectangles formed on nodes
        self.lineslist = []
        self.rect = None
        self.tmplines = []
        self.tmpcolor = []

    def deleteObj(self):
        poly = self.polyArr[self.selectedP]
        self.polylist.removePolygon(poly)
        self.polyArr = Polylist.getPolygons(self.polylist)
        self.plistbox.delete('0', 'end')
        n = 0
        print("arrcounter:")
        print(self.arrCounter)
        while n != self.arrCounter:
            self.plistbox.insert(END, n)
            n += 1
        self.redrawLine()
        self.btn_delo.config(state=DISABLED)
        self.arrCounter -= 1

    def deleteNode(self):
        poly = self.polyArr[self.selectedP]
        nodelist = Polygon.getNodes(poly)
        node = nodelist[self.selectedN]
        Polygon.removeNode(poly, node)
        self.redrawLine()

    def addNode(self):
        poly = self.polyArr[self.selectedP]
        nodeslist = Polygon.getNodes(poly)
        prev = nodeslist[self.selectedN]
        node = Node(Point(100, 100))
        Polygon.insertAfter(poly, prev, node)
        self.redrawLine()

    def redrawLine(self):
        print("function redrawline")
        del self.tmpcolor[:]
        e = len(self.polyArr)
        i = 0
        while i < e:
            lines = self.lineslist[i]
            item = lines[0]
            self.tmpcolor.append(self.canvas.itemcget(item, "fill"))
            i += 1

        # self.canvas.delete('node')
        # self.canvas.delete('pline')
        self.canvas.delete('all')
        self.updateNode(self.selectedP)
        k = 0
        m = len(self.polyArr)
        while k != m:
            poly = self.polyArr[k]
            nodeslist = Polygon.getNodes(poly)
            x = len(nodeslist)
            n = 0
            tmplines = []
            while n < x:
                if n == (x - 1):
                    n1 = nodeslist[n].getData()
                    n2 = nodeslist[0].getData()
                    x1 = n1.x
                    y1 = n1.y
                    x2 = n2.x
                    y2 = n2.y
                    l = self.canvas.create_line(x1, y1, x2, y2, tags="pline", fill=self.tmpcolor[k])
                    tmplines.append(l)
                else:
                    n1 = nodeslist[n].getData()
                    n2 = nodeslist[n + 1].getData()
                    x1 = n1.x
                    y1 = n1.y
                    x2 = n2.x
                    y2 = n2.y
                    l = self.canvas.create_line(x1, y1, x2, y2, tags="pline", fill=self.tmpcolor[k])
                    tmplines.append(l)
                n += 1

            self.lineslist[k] = tmplines
            k += 1

        self.editPoly()

    def changeColor(self):
        color = askcolor(color="blue")
        n = self.selectedP
        lines = self.lineslist[n]
        x = 0
        changeto = str(color[1])
        while x < len(lines):
            self.canvas.itemconfig(lines[x], fill=changeto)
            x += 1

    def editPoly(self):
        self.btn_pointer.config(state=ACTIVE)
        del self.rectslist[:]
        tmprects = []
        nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        n = 0
        while n < len(nodelist):
            self.rectonNode(nodelist[n], "lightblue", n, tmprects)
            n += 1
        self.rectslist.append(tmprects)
        print("selected poly: " + str(self.selectedP))
        self.canvas.bindtags((self.canvas, self.master, "all"))
        self.canvas.unbind('<Double-Button-1>')
        self.canvas.tag_bind("node", "<Button-1>", self.onclick)
        self.canvas.bind("<ButtonRelease-1>", self.onUp)

    def onclick(self, event):
        # item = self.canvas.find_closest(event.x, event.y)
        item = event.widget.find_withtag('current')[0]
        searchTags = self.canvas.gettags(item)
        print("node " + str(searchTags[1]))
        n = int(searchTags[1])
        nodeslist = Polygon.getNodes(self.polyArr[self.selectedP])
        self.selectedN = n
        self.selectedNobj = nodeslist[n]
        nodedata = nodeslist[n].getData()
        print(nodedata.x, nodedata.y)
        # rectlist = self.rectslist[self.selectedP]
        rectlist = self.rectslist[0]
        rect = rectlist[n]
        clist = self.canvas.coords(rect)
        x1 = clist[0]
        y1 = clist[1]
        x2 = clist[2]
        y2 = clist[3]
        # print(x1, y1, x2, y2)
        self.rect = rect
        self.canvas.tag_bind('node', "<Motion>", self.onDrag)

    def onDrag(self, event):
        x = event.x
        y = event.y
        s = 5
        x1 = x - s
        y1 = y - s
        x2 = x + s
        y2 = y + s
        self.canvas.coords(self.rect, (x1, y1, x2, y2))
        nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        lines = self.lineslist[self.selectedP]
        n = self.selectedN
        if n == len(nodelist) - 1:
            n0 = nodelist[n - 1].getData()
            n1 = nodelist[0].getData()
            l1 = lines[n - 1]
            l2 = lines[n]
            xol1 = n0.x
            yol1 = n0.y
            xol2 = n1.x
            yol2 = n1.y
            self.canvas.coords(l1, (xol1, yol1, x, y))
            self.canvas.coords(l2, (x, y, xol2, yol2))

        elif 0 < n < len(nodelist) - 1:
            n0 = nodelist[n - 1].getData()
            n1 = nodelist[n + 1].getData()
            l1 = lines[n - 1]
            l2 = lines[n]
            xol1 = n0.x
            yol1 = n0.y
            xol2 = n1.x
            yol2 = n1.y
            self.canvas.coords(l1, (xol1, yol1, x, y))
            self.canvas.coords(l2, (x, y, xol2, yol2))

        elif n == 0:
            n0 = nodelist[-1].getData()
            n1 = nodelist[n + 1].getData()
            l1 = lines[-1]
            l2 = lines[n]
            xol1 = n0.x
            yol1 = n0.y
            xol2 = n1.x
            yol2 = n1.y
            self.canvas.coords(l1, (xol1, yol1, x, y))
            self.canvas.coords(l2, (x, y, xol2, yol2))

    def onUp(self, event):
        self.canvas.tag_unbind('node', "<Motion>")
        nodeslist = Polygon.getNodes(self.polyArr[self.selectedP])
        n = nodeslist[self.selectedN]
        Node.setData(n, Point(event.x, event.y))
        print(event.x, event.y)
        self.selectedN = None

    def rectonNode(self,
                   node,  # Type: Node
                   color,  # Type: str
                   n,  # Type: int
                   arr  # Type: list
                   ):
        s = 5
        ndata = node.getData()
        x1 = ndata.x - s
        y1 = ndata.y - s
        x2 = ndata.x + s
        y2 = ndata.y + s
        item = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=("node", n))
        arr.append(item)

    def changeSelectedp(self, event):
        # self.btn_editP.configure(state=ACTIVE)
        self.canvas.delete('node')
        # self.rectslist = []
        curr = event.widget
        selectedP = int(curr.curselection()[0])
        self.updateNode(selectedP)
        self.selectedP = selectedP
        # self.btn_editP.config(state=ACTIVE)
        self.editPoly()
        self.btn_color.config(state=ACTIVE)
        self.btn_add.config(state=ACTIVE)
        self.btn_del.config(state=ACTIVE)
        self.btn_delo.config(state=ACTIVE)

    def updatePoly(self):
        self.plistbox.insert(END, self.arrCounter)
        self.pointer()
        print("total lines: " + str(len(self.lineslist)))

    def updateNode(self,
                   selectedPoly  # Type: int
                   ):
        self.nlistbox.delete('0', 'end')
        nodelist = Polygon.getNodes(self.polyArr[selectedPoly])
        n = 0
        while n < len(nodelist):
            self.nlistbox.insert(END, n)
            n += 1

    def changeSelectedn(self, event):
        curr = event.widget
        selectedN = int(curr.curselection()[0])
        print(selectedN)
        self.selectNode(selectedN)

    def selectNode(self,
                   selectedN  # Type: int
                   ):
        nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        nodedata = nodelist[selectedN].getData()
        print(nodedata.x, nodedata.y)

    def polyInit(self):
        self.btn_pointer.configure(state=DISABLED)
        newPoly = Polygon()
        self.polylist.insertLast(newPoly)
        self.polyArr = self.polylist.getPolygons()
        # self.polyArr.append(newPoly)
        self.arrCounter = self.arrCounter + 1
        print("Current Polygon: " + str(self.arrCounter))
        self.btn_poly.config(state=DISABLED)
        # self.btn_pointer.config(state=ACTIVE)
        self.bind()

    def pointer(self):
        # self.btn_pointer.config(state=DISABLED)
        self.btn_poly.config(state=ACTIVE)
        self.btn_add.config(state=DISABLED)
        self.btn_del.config(state=DISABLED)
        self.btn_delo.config(state=DISABLED)
        self.btn_color.config(state=DISABLED)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.delete('node')
        # print("--==New Poly==--")
        # Polylist.printList(self.polyArr[self.selectedP])
        # self.tmp.head = None

    def addWindow(self):
        window = Toplevel(self.master)
        window.geometry("+500+200")
        window.title("Add Node")
        f = Frame(window, width=self.width / 4, height=self.height / 4)
        f.pack(fill="both")

        txtInfo = StringVar(f, "Info")
        lblInfo = Label(f, textvar=txtInfo)
        lblInfo.grid(column=1, row=0)

        def runThis():
            self.addNode()
            window.destroy()

        btn_add = Button(f, text="ADD", command=runThis)
        btn_add.grid(column=0, row=1, columnspan=2, sticky=W + E)
        btn_add.config(state=DISABLED)

        nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        n = 0
        option = []
        while n < len(nodelist):
            option.append(n)
            n += 1

        var1 = StringVar()
        var1.set(option[0])

        dd = OptionMenu(f, var1, *option)
        dd.grid(column=0, row=0, sticky=W + E)

        def change_dropdown(*args):
            txtInfo.set("You will add a node after Polygon " + str(self.selectedP) + " Node " + str(var1.get()))
            btn_add.config(state=ACTIVE)
            self.selectedN = int(var1.get())

        var1.trace('w', change_dropdown)

    def delWindow(self):
        window = Toplevel(self.master)
        window.geometry("+500+200")
        window.title("Delete Node")
        f = Frame(window, width=self.width / 4, height=self.height / 4)
        f.pack(fill="both")

        txtInfo = StringVar(f, "Info")
        lblInfo = Label(f, textvar=txtInfo)
        lblInfo.grid(column=1, row=0)

        def runThis():
            self.deleteNode()
            window.destroy()

        btn_del = Button(f, text="DELETE", command=runThis)
        btn_del.grid(column=0, row=1, columnspan=2, sticky=W + E)
        btn_del.config(state=DISABLED)

        nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        n = 0
        option = []
        while n < len(nodelist):
            option.append(n)
            n += 1

        var1 = StringVar()
        var1.set(option[0])

        dd = OptionMenu(f, var1, *option)
        dd.grid(column=0, row=0, sticky=W + E)

        def change_dropdown(*args):
            txtInfo.set("You will delete Node " + str(var1.get()) + " from Polygon " + str(self.selectedP))
            btn_del.config(state=ACTIVE)
            self.selectedN = int(var1.get())

        var1.trace('w', change_dropdown)

    def bind(self):
        self.canvas.bind('<Button-1>', self.mousePosDown)
        self.canvas.bind('<ButtonRelease-1>', self.mousePosUp)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Double-Button-1>', self.doubleDone)

    def mousePosDown(self, event):
        x, y = event.x, event.y
        if self.polyArr[self.arrCounter].head is None:
            self.o.x = x
            self.o.y = y
            newhead = Node(Point(x, y))
            Polygon.setHead(self.polyArr[self.arrCounter], newhead)
            print("HEAD CREATED")
        x1, y1 = self.o.x, self.o.y
        self.canvas.create_line(x1, y1, x1, y1, tags="LINE")
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Motion>', self.dragLine)

    def mousePosUp(self, event):
        self.canvas.unbind('<Motion>')
        x, y = event.x, event.y
        if self.polyArr[self.arrCounter].head is not None:
            l = self.canvas.create_line(self.o.x, self.o.y, x, y, tags="pline")
            self.tmplines.append(l)
            self.canvas.unbind('<ButtonRelease-1>')
            self.bind()
            newnode = Node(Point(x, y))
            Polygon.insertLast(self.polyArr[self.arrCounter], newnode)
            self.o.x, self.o.y = x, y
            print("New Node is inserted ")
            item = self.canvas.find_withtag("LINE")
            self.canvas.delete(item)

    def dragLine(self, event):
        x2, y2 = event.x, event.y
        x1, y1 = self.o.x, self.o.y
        self.canvas.coords("LINE", (x1, y1, x2, y2))

    def doubleDone(self, event):
        n = 0
        l = self.canvas.create_line(self.o.x, self.o.y, self.polyArr[self.arrCounter].head.data.x,
                                    self.polyArr[self.arrCounter].head.data.y, tags="pline")
        self.tmplines.append(l)
        self.updatePoly()
        self.canvas.bindtags((self.canvas, self.master, "all"))
        item = self.canvas.find_withtag("LINE")
        self.canvas.delete(item)
        self.lineslist.append(self.tmplines)
        self.tmplines = []
        self.btn_poly.config(state=ACTIVE)
        self.btn_pointer.config(state=ACTIVE)

    def create(self):
        self.canvas = Canvas(self.master, width=self.width, height=self.height, bg="#ffffff")
        self.canvas.pack()

    def clear(self):
        self.canvas.destroy()
        self.create()
        self.pointer()
        self.polylist.head = None
        self.polyArr = []
        self.arrCounter = -1
        self.current = None
        self.selectedP = None  # passing selected polygon (int)
        self.selectedN = None  # passing selected node (int)
        self.rectslist = []  # list of polygon rectangles formed on nodes
        self.lineslist = []
        self.plistbox.delete('0', 'end')
        self.nlistbox.delete('0', 'end')

    def motion(self, event):
        x, y = event.x, event.y
        # print('{}, {}'.format(x, y))
        self.lbl_text_mousepos.set('{}, {}'.format(x, y))


root = Tk()
run = mainWindow(root)
root.mainloop()
