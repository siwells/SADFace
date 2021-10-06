import json
import sadface

"""
An empty list is used as a place holder for keeping track of old and new IDs, 
as new nodes are created they are passed into the list along with their old
ID from the AIF document. The list is used to match old IDs to new IDs when
creating edges.
"""
nodes_placeholder = []


def init(file):
    sadface.sd = sadface.initialise()
    with open(file, encoding='utf-8') as f:
        data = json.loads(f.read())
    process_data(data)


def process_data(data):
    """
    The data from the AIF JSON file is read and parsed into atoms and edges
    based on whether the AIF nodes are I nodes or S nodes, they parsed as SADFace
    atoms or schemes
    """
    for node in data['nodes']:
        if node['type'] == 'I':
            process_atom(node)
        else:
            process_scheme(node)
    for edge in data['edges']:
        process_edge(edge)
    nodes_placeholder.clear()


def process_atom(node):
    new_atom = sadface.add_atom(text=node['text'])
    new_node = {
        "old_id": node['nodeID'],
        "new_id": new_atom['id']
    }
    sadface.add_atom_metadata(new_atom['id'], 'aif_json', key='timestamp', value=node['timestamp'])
    nodes_placeholder.append(new_node)


def process_scheme(node):
    if 'scheme' in node:
        new_scheme = sadface.add_scheme(name=node['scheme'])
        new_node = {
            "old_id": node['nodeID'],
            "new_id": new_scheme['id']
        }
        sadface.add_scheme_metadata(new_scheme['id'], 'aif_json', key='timestamp', value=node['timestamp'])
        sadface.add_scheme_metadata(new_scheme['id'], 'aif_json', key='type', value=node['type'])
        nodes_placeholder.append(new_node)
    else:
        new_scheme = sadface.add_scheme(name=node['text'])
        new_node = {
            "old_id": node['nodeID'],
            "new_id": new_scheme['id']
        }
        sadface.add_scheme_metadata(new_scheme['id'], 'aif_json', key='timestamp', value=node['timestamp'])
        sadface.add_scheme_metadata(new_scheme['id'], 'aif_json', key='type', value=node['type'])
        nodes_placeholder.append(new_node)


def process_edge(edge):
    from_node = get_matching_node(edge['fromID'])
    to_node = get_matching_node(edge['toID'])
    if from_node and to_node is not None:
        sadface.add_edge(source_id=from_node, target_id=to_node)
    else:
        pass


def get_matching_node(old_node_id):
    try:
        for node in nodes_placeholder:
            if node['old_id'] == old_node_id:
                return node['new_id']
    except Exception as e:
        raise Exception(e)
