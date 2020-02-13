class Point:
    def __init__(self,
                 x,  # type: int
                 y  # type: int
                 ):
        self.x = x
        self.y = y


class Node:
    def __init__(self,
                 data  # Type: Point
                 ):
        self.data = data
        self.isEnd = False
        self.next = None

    def getData(self):
        return self.data

    def setData(self,
                data  # Type: Point
                ):
        self.data = data


class Polygon:
    def __init__(self):
        self.head = None
        self.id = "gon"
        self.next = None

    def setHead(self,
                node  # Type: Node
                ):
        self.head = node

    def getNodes(self):
        printNode = self.head
        tmplist = []
        while printNode.isEnd is not True:
            tmplist.append(printNode)
            printNode = printNode.next
        return tmplist  # returns array of nodes

    def printList(self):
        printNode = self.head
        while printNode.isEnd is not True:
            print(printNode.data.x, printNode.data.y)
            printNode = printNode.next

    def insertFirst(self,
                    node  # Type: Node
                    ):
        newNode = node
        newNode.next = self.head
        self.head = newNode

    def insertLast(self,
                   node  # Type: Node
                   ):
        newNode = node
        if self.head is None:
            self.head = newNode
            return
        lastelement = self.head
        while lastelement.next:
            lastelement = lastelement.next
        lastelement.next = newNode

    def insertAfter(self,
                    prevnode,  # Type: Node
                    node  # Type: Node
                    ):
        if prevnode is None:
            print("The mentioned node is absent")
            return
        newNode = node
        newNode.next = prevnode.next
        prevnode.next = newNode

    def removeNode(self,
                   node  # Type: Node
                   ):
        head = self.head
        prev = None
        if head is not None:
            if head == node:
                self.head = head.next
                head = None
                return

        while head is not None:
            if head == node:
                break
            prev = head
            head = head.next

        if head is None:
            return

        prev.next = head.next
        head = None

    def setDone(self):
        curr = self.head
        if self.head is None:
            return
        else:
            while curr.next:
                curr = curr.next
            curr.isEnd = True
            curr.next = self.head


class Polyline:
    def __init__(self):
        self.head = None
        self.id = "line"
        self.next = None

    def setHead(self,
                node  # Type: Node
                ):
        self.head = node

    def getNodes(self):
        printNode = self.head
        tmplist = []
        while printNode is not None:
            tmplist.append(printNode)
            printNode = printNode.next
        return tmplist  # returns array of nodes

    def printList(self):
        printNode = self.head
        while printNode is not None:
            print(printNode.data.x, printNode.data.y)
            printNode = printNode.next

    def insertFirst(self,
                    node  # Type: Node
                    ):
        newNode = node
        newNode.next = self.head
        self.head = newNode

    def insertLast(self,
                   node  # Type: Node
                   ):
        newNode = node
        if self.head is None:
            self.head = newNode
            return
        lastelement = self.head
        while lastelement.next:
            lastelement = lastelement.next
        lastelement.next = newNode

    def insertAfter(self,
                    prevnode,  # Type: Node
                    node  # Type: Node
                    ):
        if prevnode is None:
            print("The mentioned node is absent")
            return
        newNode = node
        newNode.next = prevnode.next
        prevnode.next = newNode

    def removeNode(self,
                   node  # Type: Node
                   ):
        head = self.head
        prev = None
        if head is not None:
            if head == node:
                self.head = head.next
                head = None
                return

        while head is not None:
            if head == node:
                break
            prev = head
            head = head.next

        if head is None:
            return

        prev.next = head.next
        head = None


class Polylist:
    def __init__(self):
        self.head = None

    def setHead(self,
                poly  # Type: Polygon
                ):
        self.head = poly

    def getPolys(self):
        printPolygon = self.head
        tmplist = []
        while printPolygon is not None:
            tmplist.append(printPolygon)
            printPolygon = printPolygon.next
        return tmplist  # returns array of polygons

    def insertFirst(self,
                    poly  # Type: Polygon
                    ):
        newPolygon = poly
        newPolygon.next = self.head
        self.head = newPolygon

    def insertLast(self,
                   poly  # Type: Polygon
                   ):
        newPolygon = poly
        if self.head is None:
            self.head = newPolygon
            return
        lastelement = self.head
        while lastelement.next:
            lastelement = lastelement.next
        lastelement.next = newPolygon

    def insertAfter(self,
                    prevpoly,  # Type: Polygon
                    poly  # Type: Polygon
                    ):
        if prevpoly is None:
            print("The mentioned poly is absent")
            return
        newPolygon = poly
        newPolygon.next = prevpoly.next
        prevpoly.next = newPolygon

    def removePolys(self,
                    poly  # Type: Polygon
                    ):
        head = self.head
        prev = None
        if head is not None:
            if head == poly:
                self.head = head.next
                head = None
                return

        while head is not None:
            if head == poly:
                break
            prev = head
            head = head.next

        if head is None:
            return

        prev.next = head.next
        head = None
