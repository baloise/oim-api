import xml.etree.ElementTree as ET
from datetime import datetime

class OrderHandler:

    def __init__(self, filename):
        self.filename = filename
        self.tree=ET.parse(self.filename)

    def parse_file(self):
        root = self.tree.getroot()
        for elem in root:
            print(elem.tag)
            for subelem in elem:
                print(subelem.attrib)

    def listItems(self, tag):
        root = self.tree.getroot()
        for elem in root:
            for subelem in elem.findall(tag):
                print(subelem.get('name'))

    def list_orders(self, orderno=None):
        root = self.tree.getroot()
        for elem in root.iter('order'):
            status = elem.find('status').text
            print("Orderno: {0}, Status: {1}".format(elem.get('nr'), status))

    def add(self):
        orderno=datetime.utcnow().strftime("%s%f")  # Generate unique ID
        order=ET.Element('order')
        status=ET.SubElement(order,'status')
        order.set('nr',orderno)
        status.text='open'
        print(orderno)
        root = self.tree.getroot()                  # Insert new child to structure
        root.append(order)
        newdata = ET.tostring(root,encoding='unicode')
        xmlfile=open(self.filename, "w")    # Mutex to prevent concurrent reads/writes on the same file from multiple instances
        xmlfile.write(newdata)              # Save the file
        return orderno

    def get_status(self,orderno):
        root = self.tree.getroot()
        res=filter(lambda x: orderno in x.get('nr'), root.findall('.//order[@nr]'))
        for i in res:
            for c in i.getchildren():  #  sollte 'status' finden, nicht jede Kinder
                return c.text

    #def update_status(self,status):
        #with self.filemutex:


if __name__ == '__main__':
    writer = OrderHandler('order_data.xml')
    writer.list_orders()
    print(writer.add())
    print(writer.get_status('3'))

