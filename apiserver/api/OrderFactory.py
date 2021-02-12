import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime


class OrderFactory:

    def __init__(self, filename):
        self.filename = filename
        if not Path(self.filename).exists():
            tree = ET.Element('data')
            newdata = ET.tostring(tree, encoding='unicode', method='xml')
            xmlfile = open(self.filename, "w")
            xmlfile.write(newdata)
            xmlfile.close()
        self.tree = ET.parse(self.filename)

    def generate_order(self, requester_id='b0123456', bu='BU 401', order_type='VM', description=None):      # noqa
        order = ET.Element('order')
        erequester_id = ET.SubElement(order, 'requester_id')
        erequester_id.text = requester_id
        ecreation_date = ET.SubElement(order, 'creation_date')
        ecreation_date.text = datetime.ctime(datetime.utcnow())
        ebu = ET.SubElement(order, 'business_unit')
        ebu.text = bu
        eorder_type = ET.SubElement(order, 'order_type')
        eorder_type.text = order_type
        edescription = ET.SubElement(order, 'description')
        edescription.text = description
        estatus = ET.SubElement(order, 'status')
        estatus.text = 'open'
        orderid = datetime.utcnow().strftime("%s%f")
        order.set('id', orderid)
        root = self.tree.getroot()
        root.append(order)
        newdata = ET.tostring(root, encoding='unicode')

        def make_pretty(data):
            return '\n'.join([
                line for line in minidom.parseString(data).toprettyxml(indent=' '*2).split('\n') if line.strip()
                ])  # noqa

        xmlfile = open(self.filename, "w")
        xmlfile.write(make_pretty(newdata))
        return orderid

    def list_orders(self):
        root = self.tree.getroot()
        answer = '\n'
        for elem in root.iter('order'):
            status = elem.find('status').text
            answer += "Order id: " + elem.get('id') + "status: " + status + '\n' # noqa
        return answer

    def get_status(self, orderid):
        status = self.tree.find('.//order[@id="' + orderid + '"]/status')
        try:
            return status.text
        except Exception:
            return ''

    def get_details(self, orderid):
        order = self.tree.find('.//order[@id="' + orderid + '"]')
        if order:
            answer = '\n'
            for item in list(order):
                answer += item.tag+' : ' + item.text + '\n'
            return answer
        else:
            return ''


if __name__ == '__main__':
    factory = OrderFactory('orders_data.xml')
    #  factory.generate_order(requester_id='b039214', description='This is my order')   # noqa
    print(factory.get_status('1613028463047852'))
    print(factory.get_details('1613039330628156'))
    print(factory.list_orders())
