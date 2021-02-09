import xml.etree.ElementTree as ET

class OrderHandler:


  def parseFile(self, filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for elem in root:
      print(elem.tag)
      for subelem in elem:
        print(subelem.attrib)


  def listItems(self, tag):
    tree = ET.parse(self.filename)
    root = tree.getroot()
    for elem in root:
      for subelem in elem.findall(tag):
        print(subelem.get('name'))


  def listOrders(self, orderno=None):
    tree = ET.parse(self.filename)
    root = tree.getroot()
    for elem in root.iter('order'):
      status=elem.find('status').text
      print("Orderno: {0}, Status: {1}".format(elem.get('nr'), status))


  def __init__(self, filename):
    self.filename=filename


writer=OrderHandler('order_data.xml')
#writer.parseFile('order_data.xml')
writer.listOrders()
