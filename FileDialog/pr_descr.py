#encoding = utf-8
from xml.etree.ElementTree import *

def read_xml(in_path):
    '''
    :param in_path:
    :return:
    '''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def write_xml(tree,out_path):
    '''

    :param tree:
    :param out_path:
    :return:
    '''
    ##tree.write(out_path, "/t", "/n", encoding="utf-8", xml_declaration=True)

def if_match(node, kv_map):
    '''

    :param node:
    :param kv_map:
    :return:
    '''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False

    return True

def create_node(tag, property_map, content):
    '''

    :param tag:
    :param property_map:
    :param content:
    :return:
    '''
    element = Element(tag,property_map)
    element.text = content
    return element

def find_nodes(tree,path):
    '''

    :param tree:
    :param path:
    :return:
    '''
    return tree.findall(path)

def get_node_by_keyvalue(nodelist, kv_map):
    '''

    :param nodelist:
    :param kv_map:
    :return:
    '''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)

    return result_nodes

def add_child_node(nodelist,element):
    '''

    :param nodelist:
    :param element:
    :return:
    '''
    for node in nodelist:
        node.append(element)

if __name__ == "__main__":
    # 1. Read xml file
    tree = read_xml('C:/ZDC/d_excel.xml')
    root = tree.getroot()
    #nodes = find_nodes(tree, "data")
    #result_nodes = get_node_by_keyvalue(nodes,{"name":"AIB"})

    #a = create_node("FAM",{"name":"AUD"}, "Des_de")
    a = Element("FAM",{"name":"AUD"})
    b = SubElement(a, "Des_de")

    b.text = "MultimediaVideo/-DVD/Notebook-Anschlu~ "

    c = SubElement(a, "Des_cn")
    c.text = "..."

    d = SubElement(a, "PR")
    d.attrib = {"name":"9WC"}

    e = SubElement(d,"Des_de")
    e.text = "Ohne Multimedia im Fahrzeug "
    f = SubElement(d,"Des_cn")
    f.text = "klll"

    #add_child_node(root,a)
    root.append(a)

    #write_xml(tree,"./out0.xml")

    tree.write("./out0.xml", encoding='utf-8', method='xml')




