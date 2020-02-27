from Tkinter import *
from dataStructs import *
from tkcolorpicker import *
import tkFileDialog
import math
import os
import tkMessageBox


class mainWindow:
    def __init__(self, master):
        self.master = master
        master.title("testPolygon")
        master.geometry("+300+100")
        self.width = 640
        self.height = 480

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open...", command=self.open_file)
        fileMenu.add_command(label="Save...", command=self.save_file)
        menu.add_cascade(label="File", menu=fileMenu)

        calcMenu = Menu(menu)
        calcMenu.add_command(label="Perimeter & Area", command=self.calc_peri_area)
        calcMenu.add_command(label="Convex/Concave", command=self.isconvex)
        menu.add_cascade(label="Calculate", menu=calcMenu)

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

        self.btn_poly = Button(self.framelt, text="New Polygon", command=self.polygonInit)
        self.btn_poly.grid(column=0, row=1, sticky=W + E)

        self.btn_poli = Button(self.framelt, text="New Polyline", command=self.polylineInit)
        self.btn_poli.grid(column=0, row=2, sticky=W + E)

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
        self.lbl1 = Label(self.framell, text="Poly List").pack(side="top", fill="both")

        self.nlistbox = Listbox(self.framell)
        self.nlistbox.pack(side="bottom", fill="both")
        self.lbl2 = Label(self.framell, text="Poly Nodes List").pack(side="bottom", fill="both")
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
        self.shape = "polygon"

    def isconvex(self):
        # n = 0
        polylist = self.polylist.getPolys()
        # Algorithm dr sir Eddo
        # for poly in polylist:
        #     id = self.getpid(n)
        #     if id == "polygon":
        #         nodelist = Polygon.getNodes(poly)
        #         print("polygon " + str(n))
        #         out = self.method1(nodelist, poly)
        #         if out == False:
        #             print("This polygon is CONCAVE")
        #         else:
        #             print("This polygon is CONVEX")
        #     n += 1

        # Algorithm 2
        n = 0
        res = ""
        for poly in polylist:
            id = self.getpid(n)
            if id == "polygon":
                nodelist = Polygon.getNodes(poly)
                print("polygon " + str(n))
                if self.method2(nodelist):
                    res += "polygon " + str(n) + " is Convex\n"
                else:
                    res += "polygon " + str(n) + " is Concave\n"
            n += 1
        tkMessageBox.showinfo("Convex/Concave", res)

    def method1(self,
                      nodelist,  # Type: list
                      poly  # Type: Polygon
                      ):
        if len(nodelist) < 3:
            print("error node less than 3")
            return False
        else:
            F = poly.head
            EPrev = F
            E = F.next
            P1 = EPrev.getData()
            P2 = E.getData()
            V1 = (P2.x - P1.x, P2.y - P1.y)
            EPrev = E
            E = E.next
            P1 = EPrev.getData()
            P2 = E.getData()
            V2 = (P2.x - P1.x, P2.y - P1.y)
            c2 = V1[0] * V2[1] - V1[1] * V2[0]
            c1 = c2
            while E.next is not None and c2 * c1 > 0:
                EPrev = E
                E = E.next
                V1 = V2
                c1 = c2
                P1 = P2
                P2 = E.getData()
                V2 = (P2.x - P1.x, P2.y - P1.y)
                c2 = V1[0] * V2[1] - V1[1] - V2[0]
            if c2 * c1 > 0:
                c1 = c2
                V1 = V2
                P1 = P2
                P2 = F.getData()
                V2 = (P2.x - P1.x, P2.y - P1.y)
                c2 = V1[0] * V2[1] - V1[1] * V2[0]
            return c2 * c1 < 0

    def method2(self,
                            nodelist  # Type: Polygon
                            ):
        if len(nodelist) < 3:
            print("error node less than 3")
            return False
        else:
            wSign = 0
            xSign = 0
            xFirstSign = 0
            xFlips = 0
            ySign = 0
            yFirstSign = 0
            yFlips = 0
            curr = nodelist[-2].getData()
            next = nodelist[-1].getData()

            for v in nodelist:
                prev = curr
                curr = next
                next = v.getData()

                # Previous edge vector (before)
                bx = curr.x - prev.x
                by = curr.y - curr.y

                # Next edge vector (after)
                ax = next.x - curr.x
                ay = next.y - curr.y

                # Calculate sign flips using next edge vector (after)
                # Recording first sign
                if ax > 0:
                    if xSign == 0:
                        xFirstSign += 1
                    elif xSign < 0:
                        xFlips += 1
                    xSign += 1
                elif ax < 0:
                    if xSign == 0:
                        xFirstSign -= 1
                    elif xSign > 0:
                        xFlips += 1
                    xSign -= 1

                if xFlips > 2:
                    print("This polygon is CONCAVE")
                    return False

                if ay > 0:
                    if ySign == 0:
                        yFirstSign += 1
                    elif ySign < 0:
                        yFlips += 1
                    ySign += 1
                elif ay < 0:
                    if ySign == 0:
                        yFirstSign -= 1
                    elif ySign > 0:
                        yFlips += 1
                    ySign -= 1

                if yFlips > 2:
                    print("This polygon is CONCAVE")
                    return False

                # Find out orientation of this pair of edges,
                # and ensure it does not differ from previous ones
                w = bx * ay - ax * by
                if wSign == 0 and w is not 0:
                    wSign = w
                elif wSign > 0 and w < 0:
                    print("This polygon is CONCAVE")
                    return False
                elif wSign < 0 and w > 0:
                    print("This polygon is CONCAVE")
                    return False

            # Final/wraparound sign flips
            if xSign is not 0 and xFirstSign is not 0 and xSign is not xFirstSign:
                xFlips += 1
            if ySign is not 0 and yFirstSign is not 0 and ySign is not yFirstSign:
                yFlips += 1

            # Concave polygons have 2 sign flips along each axis
            if xFlips is not 2 and yFlips is not 2:
                print("This polygon is CONCAVE")
                return False
            else:
                print("This polygon is CONVEX")
                return True

    def calc_peri_area(self):
        n = 0
        resstr = ""
        for lineslist in self.lineslist:
            perimeter = 0
            area = 0
            id = self.getpid(n)
            if id == "polygon":
                for item in lineslist:
                    line = self.canvas.coords(item)
                    x0 = line[0]
                    y0 = line[1]
                    x1 = line[2]
                    y1 = line[3]
                    d = math.sqrt((math.pow((y1 - y0), 2)) + (math.pow((x1 - x0), 2)))
                    perimeter += d
                    area += (x1 * y0 - y1 * x0)
                    area /= 2
                    area = abs(area)
                print("Perimeter of polygon " + str(n) + " = " + str(perimeter) + " pixel")
                print("A polygon " + str(n) + " = " + str(area) + " pixel^2")
                resstr = resstr + "P polygon " + str(n) + " = " + str(perimeter) + " pixel" + "\n" + \
                         "A polygon " + str(n) + " = " + str(area) + " pixel^2" + "\n"
            else:
                for item in lineslist:
                    line = self.canvas.coords(item)
                    x0 = line[0]
                    y0 = line[1]
                    x1 = line[2]
                    y1 = line[3]
                    d = math.sqrt((math.pow((y1 - y0), 2)) + (math.pow((x1 - x0), 2)))
                    perimeter += d
                print("Perimeter of polyline " + str(n) + " = " + str(perimeter) + " pixel")
                print("Polyline doesn't have area")
                resstr = resstr + "P of polyline " + str(n) + " = " + str(perimeter) + " pixel" + "\n"
            n += 1
        tkMessageBox.showinfo("Perimeter & Area", resstr)

    def open_file(self):
        fname = tkFileDialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        result = []
        shapelist = []
        with open(fname, "r") as f:
            string = f.read()
            string = string.strip('\n')
            splitted = string.split(os.linesep + os.linesep)
            print("READING...")
            print( "# of poly(s): " + str(len(splitted)))
            for idx, i in enumerate(splitted):
                splitted2 = i.split('\n')
                pid = splitted2[0]
                pid = "poly" + pid
                print(pid)
                shapelist.append(pid)
                splitted2.pop(0)
                print("poly " + str(idx) + " have: " + str(len(splitted2)) + " nodes")
                tmparr = []
                for j in splitted2:
                    tmp = j.split(',')
                    tmparr.append((int(tmp[0]), int(tmp[1])))
                result.append(tmparr)

        print(result)
        self.reinit(result, shapelist)

    def reinit(self, plist,  # Type: list
               shapelist  # Type: list
               ):
        self.clear()
        self.polylist = Polylist()
        for i, poly in enumerate(plist):
            if shapelist[i] == "polygon":
                newpoly = Polygon()
                for node in poly:
                    np = Point(node[0], node[1])
                    newnode = Node(np)
                    newpoly.insertLast(newnode)
                newpoly.setDone() # set last node isEnd to True
                self.polylist.insertLast(newpoly)
            elif shapelist[i] == "polyline":
                newpoly = Polyline()
                for node in poly:
                    np = Point(node[0], node[1])
                    newnode = Node(np)
                    newpoly.insertLast(newnode)
                self.polylist.insertLast(newpoly)
        self.polyArr = self.polylist.getPolys()
        self.arrCounter = len(self.polyArr) - 1
        n = 0
        lgt = len(self.polyArr)
        while n < lgt:
            poly = self.polyArr[n]
            nodeslist = poly.getNodes()
            m = 0
            mgt = len(nodeslist)
            while m < mgt:
                if shapelist[n] == "polygon":
                    if m == mgt-1:
                        dt1 = nodeslist[m]
                        dt2 = nodeslist[0]
                        node1 = dt1.getData()
                        node2 = dt2.getData()
                        x1 = node1.x
                        y1 = node1.y
                        x2 = node2.x
                        y2 = node2.y
                        l = self.canvas.create_line(x1, y1, x2, y2, tags="pline")
                        self.tmplines.append(l)
                    else:
                        dt1 = nodeslist[m]
                        dt2 = nodeslist[m + 1]
                        node1 = dt1.getData()
                        node2 = dt2.getData()
                        x1 = node1.x
                        y1 = node1.y
                        x2 = node2.x
                        y2 = node2.y
                        l = self.canvas.create_line(x1, y1, x2, y2, tags="pline")
                        self.tmplines.append(l)
                elif shapelist[n] == "polyline":
                    if m == mgt-1:
                        print("end of polyline")
                    else:
                        dt1 = nodeslist[m]
                        dt2 = nodeslist[m + 1]
                        node1 = dt1.getData()
                        node2 = dt2.getData()
                        x1 = node1.x
                        y1 = node1.y
                        x2 = node2.x
                        y2 = node2.y
                        l = self.canvas.create_line(x1, y1, x2, y2, tags="pline")
                        self.tmplines.append(l)
                m += 1
            self.lineslist.append(self.tmplines)
            self.tmplines = []
            n += 1
        for idx, p in enumerate(plist):
            self.plistbox.insert(END, idx)

    def save_file(self):
        f = tkFileDialog.asksaveasfile(mode="w", defaultextension=".txt")
        fname = f.name
        if f is None:
            return
        polyarr = self.polyArr
        for poly in polyarr:
            nodes = poly.getNodes()
            f.write(poly.id + '\n')
            for node in nodes:
                data = node.getData()
                x = data.x
                y = data.y
                f.write('{}, {}'.format(x, y))
                f.write('\n')
            #     print >> f, str(x) + ", " + str(y)
            f.write('\n')
        f.close()
        # os.system("gedit " + fname)

    def deleteObj(self):
        poly = self.polyArr[self.selectedP]
        self.polylist.removePolys(poly)
        self.polyArr = Polylist.getPolys(self.polylist)
        self.tmpcolor.pop(self.selectedP)
        self.lineslist.pop(self.selectedP)
        self.plistbox.delete('0', 'end')
        n = 0
        while n != self.arrCounter:
            self.plistbox.insert(END, n)
            n += 1
        self.redrawLine()
        self.btn_delo.config(state=DISABLED)
        self.arrCounter -= 1

    def deleteNode(self):
        poly = self.polyArr[self.selectedP]
        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
            node = nodelist[self.selectedN]
            Polygon.removeNode(poly, node)
            self.redrawLine()
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
            node = nodelist[self.selectedN]
            Polyline.removeNode(poly, node)
            self.redrawLine()

    def addNode(self):
        poly = self.polyArr[self.selectedP]
        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
            prev = nodelist[self.selectedN]
            node = Node(Point(100, 100))
            Polygon.insertAfter(poly, prev, node)
            self.redrawLine()
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
            prev = nodelist[self.selectedN]
            node = Node(Point(100, 100))
            Polyline.insertAfter(poly, prev, node)
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

        self.canvas.delete('all')
        self.nlistbox.delete('0', 'end')
        k = 0
        m = len(self.polyArr)
        while k != m:
            id = self.getpid(k)
            if id == "polygon":
                nodeslist = Polygon.getNodes(self.polyArr[k])
            else:
                nodeslist = Polyline.getNodes(self.polyArr[k])
            x = len(nodeslist)
            n = 0
            tmplines = []
            while n < x:
                if n == (x - 1):
                    if id == "polygon":
                        n1 = nodeslist[n].getData()
                        n2 = nodeslist[0].getData()
                        x1 = n1.x
                        y1 = n1.y
                        x2 = n2.x
                        y2 = n2.y
                        l = self.canvas.create_line(x1, y1, x2, y2, tags="pline", fill=self.tmpcolor[k])
                        tmplines.append(l)
                else:
                    if id == "polygon":
                        n1 = nodeslist[n].getData()
                        n2 = nodeslist[n + 1].getData()
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

        # self.editPoly()

    def changeColor(self):
        color = askcolor(color="blue")
        n = self.selectedP
        lines = self.lineslist[n]
        x = 0
        changeto = str(color[1])
        self.tmpcolor[self.selectedP] = color[1]
        while x < len(lines):
            self.canvas.itemconfig(lines[x], fill=changeto)
            x += 1

    def editPoly(self):
        self.btn_pointer.config(state=ACTIVE)
        del self.rectslist[:]
        tmprects = []
        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
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
        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodeslist = Polygon.getNodes(self.polyArr[self.selectedP])
        else:
            nodeslist = Polyline.getNodes(self.polyArr[self.selectedP])
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
        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
        lines = self.lineslist[self.selectedP]
        n = self.selectedN
        if n == len(nodelist) - 1:
            if id == "polygon":
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
            else:
                n0 = nodelist[n - 1].getData()
                l1 = lines[n - 1]
                xol1 = n0.x
                yol1 = n0.y
                self.canvas.coords(l1, (xol1, yol1, x, y))

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
            if id == "polygon":
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
            else:
                n1 = nodelist[n + 1].getData()
                l2 = lines[n]
                xol2 = n1.x
                yol2 = n1.y
                self.canvas.coords(l2, (x, y, xol2, yol2))

    def onUp(self, event):
        self.canvas.tag_unbind('node', "<Motion>")
        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
        n = nodelist[self.selectedN]
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
        self.selectedP = selectedP
        self.updateNode(selectedP)
        # self.btn_editP.config(state=ACTIVE)
        self.editPoly()
        self.btn_color.config(state=ACTIVE)
        self.btn_add.config(state=ACTIVE)
        self.btn_del.config(state=ACTIVE)
        self.btn_delo.config(state=ACTIVE)

    def updatePoly(self):
        self.plistbox.insert(END, self.arrCounter)
        self.pointer()

    def updateNode(self,
                   selectedPoly  # Type: int
                   ):
        self.nlistbox.delete('0', 'end')
        id = self.getpid(selectedPoly)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[selectedPoly])
        else:
            nodelist = Polyline.getNodes(self.polyArr[selectedPoly])
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

    def polylineInit(self):
        self.shape = "polyline"
        self.btn_pointer.configure(state=DISABLED)
        newPoly = Polyline()
        self.polylist.insertLast(newPoly)
        self.polyArr = self.polylist.getPolys()
        # self.polyArr.append(newPoly)
        self.arrCounter = self.arrCounter + 1
        print("Current Polygon: " + str(self.arrCounter))
        self.btn_poly.config(state=DISABLED)
        self.btn_poli.config(state=DISABLED)
        # self.btn_pointer.config(state=ACTIVE)
        self.bind()

    def polygonInit(self):
        self.shape = "polygon"
        self.btn_pointer.configure(state=DISABLED)
        newPoly = Polygon()
        self.polylist.insertLast(newPoly)
        self.polyArr = self.polylist.getPolys()
        # self.polyArr.append(newPoly)
        self.arrCounter = self.arrCounter + 1
        print("Current Polygon: " + str(self.arrCounter))
        self.btn_poly.config(state=DISABLED)
        self.btn_poli.config(state=DISABLED)
        # self.btn_pointer.config(state=ACTIVE)
        self.bind()

    def pointer(self):
        # self.btn_pointer.config(state=DISABLED)
        self.btn_poly.config(state=ACTIVE)
        self.btn_poli.config(state=ACTIVE)
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

        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
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
            txtInfo.set("You will add a node after Poly " + str(self.selectedP) + " Node " + str(var1.get()))
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

        id = self.getpid(self.selectedP)
        if id == "polygon":
            nodelist = Polygon.getNodes(self.polyArr[self.selectedP])
        else:
            nodelist = Polyline.getNodes(self.polyArr[self.selectedP])
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
            txtInfo.set("You will delete Node " + str(var1.get()) + " from Poly " + str(self.selectedP))
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
            id = self.getpid(self.arrCounter)
            print(id)
            if id == "polygon":
                Polygon.setHead(self.polyArr[self.arrCounter], newhead)
            else:
                Polyline.setHead(self.polyArr[self.arrCounter], newhead)
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
            id = self.getpid(self.arrCounter)
            if id == "polygon":
                Polygon.insertLast(self.polyArr[self.arrCounter], newnode)
            else:
                Polyline.insertLast(self.polyArr[self.arrCounter], newnode)
            self.o.x, self.o.y = x, y
            print("New Node is inserted ")
            item = self.canvas.find_withtag("LINE")
            self.canvas.delete(item)

    def dragLine(self, event):
        x2, y2 = event.x, event.y
        x1, y1 = self.o.x, self.o.y
        self.canvas.coords("LINE", (x1, y1, x2, y2))

    def getpid(self,
               n  # Type: int
               ):
        plist = self.polylist.getPolys()
        p = plist[n]
        id = p.id
        id = "poly" + str(id)
        return id

    def doubleDone(self, event):
        id = self.getpid(self.arrCounter)
        if id == "polygon":
            l = self.canvas.create_line(self.o.x, self.o.y, self.polyArr[self.arrCounter].head.data.x,
                                        self.polyArr[self.arrCounter].head.data.y, tags="pline")
            self.tmplines.append(l)

        self.updatePoly()
        self.canvas.bindtags((self.canvas, self.master, "all"))
        item = self.canvas.find_withtag("LINE")
        self.canvas.delete(item)
        self.lineslist.append(self.tmplines)
        self.tmplines = []
        self.tmpcolor.append("#000000")
        self.btn_poly.config(state=ACTIVE)
        self.btn_pointer.config(state=ACTIVE)
        self.btn_poli.config(state=ACTIVE)
        if id == "polygon":
            if self.polyArr[self.arrCounter].head is not None:
                poly = self.polyArr[self.arrCounter]
                poly.setDone()

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
