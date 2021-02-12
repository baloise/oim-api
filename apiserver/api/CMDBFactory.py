import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime


class CMDBFactory:

    def __init__(self, filename):
        self.filename = filename
        if not Path(self.filename).exists():
            tree = ET.Element('data')
            newdata = ET.tostring(tree, encoding='unicode', method='xml')
            xmlfile = open(self.filename, "w")
            xmlfile.write(newdata)
            xmlfile.close()
        self.tree = ET.parse(self.filename)

    def generate_item(self, name, itype, requester_id='b0123456', description=None):    # noqa
        item = ET.Element('item')
        ename = ET.SubElement(item, 'name')
        ename.text = name
        etype = ET.SubElement(item, 'type')
        etype.text = itype
        eparentid = ET.SubElement(item, 'parentid')
        eparentid.text = '0'
        erequester_id = ET.SubElement(item, 'requester_id')
        erequester_id.text = requester_id
        ecreated = ET.SubElement(item, 'created')
        ecreated.text = datetime.ctime(datetime.utcnow())
        eorderid = ET.SubElement(item, 'orderid')
        eorderid.text = datetime.utcnow().strftime("%s%f")
        edescription = ET.SubElement(item, 'description')
        edescription.text = description
        itemid = datetime.utcnow().strftime("%s%f")
        item.set('id', itemid)
        root = self.tree.getroot()
        root.append(item)
        newdata = ET.tostring(root, encoding='unicode')

        def make_pretty(data):
            return '\n'.join([
                line for line in minidom.parseString(data).toprettyxml(indent=' '*2).split('\n') if line.strip()
                ])    # noqa

        xmlfile = open(self.filename, "w")
        xmlfile.write(make_pretty(newdata))
        return itemid

    def list_items(self):
        root = self.tree.getroot()
        answer = '\n'
        for elem in root.iter('item'):
            name = elem.find('name').text
            answer += "Item id: " + elem.get('id') + " name: "+ name + '\n' # noqa
        return answer

    def get_id(self, iname):
        root = self.tree.getroot()
        answer = '\n'
        for elem in root.iter('item'):
            name = elem.find('name').text
            if name.__contains__(iname):
                answer += "Item id: " + elem.get('id') + " name: "+ name + '\n' # noqa
        return answer

    def get_info(self, itemid):
        item = self.tree.find('.//item[@id="'+itemid+'"]')
        if item:
            answer = '\n'
            for attrib in list(item):
                answer += attrib.tag+' : '+attrib.text+'\n'
            return answer
        else:
            return ''


if __name__ == '__main__':
    factory = CMDBFactory('cmdb_data.xml')
    itemid = factory.generate_item('svw-blablat003', 'VM', requester_id='b088881', description='This is my blabla VM')  # noqa
    print("New item", itemid)
    print(factory.list_items())
    print(factory.get_info('1613044439027152'))
    print(factory.list_items())
