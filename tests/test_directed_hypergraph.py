from __future__ import absolute_import

from hypergraph.directed_hypergraph import DirectedHypergraph


def test_add_node():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}

    # Test adding unadded nodes with various attribute settings
    H = DirectedHypergraph()
    H.add_node(node_a)
    H.add_node(node_b, source=True)
    H.add_node(node_c, attrib_c)
    H.add_node(node_d, attrib_d, sink=False)

    assert node_a in H.node_attributes
    assert H.node_attributes[node_a] == {}
    
    assert node_b in H.node_attributes
    assert H.node_attributes[node_b]['source'] == True
    
    assert node_c in H.node_attributes
    assert H.node_attributes[node_c]['alt_name'] == 1337
    
    assert node_d in H.node_attributes
    assert H.node_attributes[node_d]['label'] == 'black'
    assert H.node_attributes[node_d]['sink'] == False

    # Test adding a node that has already been added
    H.add_nodes(node_a, common=False)
    assert H.node_attributes[node_a]['common'] == False


def test_add_nodes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    common_attrib = {'common': True, 'source': False}
    
    node_list = [node_a, (node_b, {'source': False}), (node_c, attrib_c), (node_d, attrib_d)]

    # Test adding unadded nodes with various attribute settings
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)

    assert node_a in H.node_attributes
    assert H.node_attributes[node_a] == common_attrib
    
    assert node_b in H.node_attributes
    assert H.node_attributes[node_b]['source'] == False
    
    assert node_c in H.node_attributes
    assert H.node_attributes[node_c]['alt_name'] == 1337
    
    assert node_d in H.node_attributes
    assert H.node_attributes[node_d]['label'] == 'black'
    assert H.node_attributes[node_d]['sink'] == True


def test_add_hyperedge():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'

    tail = set([node_a, node_b]); frozen_tail = frozenset(tail)
    head = set([node_c, node_d]); frozen_head = frozenset(head)
    attrib = {'weight': 6, 'color': 'black'}

    H = DirectedHypergraph()
    H.add_node(node_a, label=1337)
    H.add_hyperedge(tail, head, attrib, weight=5)

    # Test that all hyperedge attributes are correct
    assert H.hyperedge_attributes['e1']['tail'] == tail
    assert H.hyperedge_attributes['e1']['head'] == head
    assert H.hyperedge_attributes['e1']['weight'] == 5

    # Test that successor list contains the correct info
    assert frozen_head in H.successors[frozen_tail]
    assert 'e1' in H.successors[frozen_tail][frozen_head]

    # Test that the precessor list contains the correct info
    assert frozen_tail in H.predecessors[frozen_head]
    assert 'e1' in H.predecessors[frozen_head][frozen_tail]
