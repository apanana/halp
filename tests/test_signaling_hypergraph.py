from os import remove

from halp.signaling_hypergraph import SignalingHypergraph


def test_add_node():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}

    # Test adding unadded nodes with various attribute settings
    H = SignalingHypergraph()
    H.add_node(node_a)
    H.add_node(node_b, source=True)
    H.add_node(node_c, attrib_c)
    H.add_node(node_d, attrib_d, sink=False)

    assert node_a in H._node_attributes
    assert H._node_attributes[node_a] == {"__in_hypernodes":set()}

    assert node_b in H._node_attributes
    assert H._node_attributes[node_b]['source'] is True

    assert node_c in H._node_attributes
    assert H._node_attributes[node_c]['alt_name'] == 1337

    assert node_d in H._node_attributes
    assert H._node_attributes[node_d]['label'] == 'black'
    assert H._node_attributes[node_d]['sink'] is False

    # Test adding a node that has already been added
    H.add_node(node_a, common=False)
    assert H._node_attributes[node_a]['common'] is False

    # Pass in bad (non-dict) attribute
    try:
        H.add_node(node_a, ["label", "black"])
        assert False
    except AttributeError:
        pass
    except BaseException as e:
        assert False, e

def test_add_nodes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    common_attrib = {'common': True, 'source': False}

    node_list = [node_a, (node_b, {'source': False}),
                 (node_c, attrib_c), (node_d, attrib_d)]

    # Test adding unadded nodes with various attribute settings
    H = SignalingHypergraph()
    H.add_nodes(node_list, common_attrib)

    common_attrib["__in_hypernodes"] = set()

    assert node_a in H._node_attributes
    assert H._node_attributes[node_a] == common_attrib

    assert node_b in H._node_attributes
    assert H._node_attributes[node_b]['source'] is False

    assert node_c in H._node_attributes
    assert H._node_attributes[node_c]['alt_name'] == 1337

    assert node_d in H._node_attributes
    assert H._node_attributes[node_d]['label'] == 'black'
    assert H._node_attributes[node_d]['sink'] is True

def test_get_node_set():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    common_attrib = {'common': True, 'source': False}

    node_list = [node_a, (node_b, {'source': False}),
                 (node_c, attrib_c), (node_d, attrib_d)]

    # Test adding unadded nodes with various attribute settings
    H = SignalingHypergraph()
    H.add_nodes(node_list, common_attrib)
    node_set = H.get_node_set()
    assert node_set == set(['A', 'B', 'C', 'D'])
    assert len(node_set) == len(node_list)
    for node in H.node_iterator():
        assert node in node_set

def test_node_iterator():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    common_attrib = {'common': True, 'source': False}

    node_list = [node_a, (node_b, {'source': False}),
                 (node_c, attrib_c), (node_d, attrib_d)]

    # Test adding unadded nodes with various attribute settings
    H = SignalingHypergraph()
    H.add_nodes(node_list, common_attrib)
    node_set = H.get_node_set()

    for node in H.node_iterator():
        assert node in node_set

def test_add_hypernode():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'

    hypernode_a = 'Ha'
    attrib_ha = {'alt_name': 1337}

    # Test adding unadded nodes with various attribute settings
    H = SignalingHypergraph()
    H.add_nodes([node_a, node_b, node_c])
    H.add_hypernode(hypernode_a, set([node_a, node_b, node_c]),attrib_ha, source=True)


    assert node_a in H._node_attributes
    assert H._node_attributes[node_a] == {"__in_hypernodes":set([hypernode_a])}

    assert node_b in H._node_attributes
    assert H._node_attributes[node_b] == {"__in_hypernodes":set([hypernode_a])}

    assert node_c in H._node_attributes
    assert H._node_attributes[node_c] == {"__in_hypernodes":set([hypernode_a])}

    assert hypernode_a in H._hypernode_attributes
    assert H._hypernode_attributes[hypernode_a]['source'] is True

    # Test adding a node that has already been added
    H.add_hypernode(hypernode_a, common=False)
    assert H._hypernode_attributes[hypernode_a]['common'] is False

    # Pass in bad (non-dict) attribute
    try:
        H.add_hypernode(hypernode_a, ["label", "black"])
        assert False
    except AttributeError:
        pass
    except BaseException as e:
        assert False, e

def test_add_hypernodes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'

    hypernode_a = 'Ha'
    attrib_ha = {'alt_name': 1337}
    hypernode_b = 'Hb'

    # Test adding unadded nodes with various attribute settings
    H = SignalingHypergraph()
    H.add_nodes([node_a, node_b, node_c, node_d, node_e])
    H.add_hypernode(hypernode_a, set([node_a, node_b, node_c]),attrib_ha, source=True)


    assert node_a in H._node_attributes
    assert H._node_attributes[node_a] == {"__in_hypernodes":set([hypernode_a])}

    assert node_b in H._node_attributes
    assert H._node_attributes[node_b] == {"__in_hypernodes":set([hypernode_a])}

    assert node_c in H._node_attributes
    assert H._node_attributes[node_c] == {"__in_hypernodes":set([hypernode_a])}

    assert hypernode_a in H._hypernode_attributes
    assert H._hypernode_attributes[hypernode_a]['source'] is True

    # Test adding a node that has already been added
    H.add_hypernode(hypernode_a, common=False)
    assert H._hypernode_attributes[hypernode_a]['common'] is False

    # Pass in bad (non-dict) attribute
    try:
        H.add_hypernode(hypernode_a, ["label", "black"])
        assert False
    except AttributeError:
        pass
    except BaseException as e:
        assert False, e

def test_add_hyperedge():
    # Ha = (A,B,C)
    # Hb = (D,E)
    # Hc = (C,F)
    # e1 = (Ha,Hb)->(Hc)

    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    node_f = 'F'

    hypernode_a = 'Ha'
    hypernode_b = 'Hb'
    hypernode_c = 'Hc'

    H = SignalingHypergraph()

    # H.add_nodes([node_a, node_b, node_c, node_d, node_e, node_f])
    # H.add_hypernode(hypernode_a, set([node_a, node_b, node_c]))
    # H.add_hypernode(hypernode_b, set([node_d, node_e]))
    # H.add_hypernode(hypernode_c, set([node_c, node_f]))

    tail = set([hypernode_a, hypernode_b])
    head = set([hypernode_c])
    frozen_tail = frozenset(tail)
    frozen_head = frozenset(head)
    attrib = {'weight': 6, 'color': 'black'}

    hyperedge_name = H.add_hyperedge(tail, head, attr_dict=attrib, weight=5) 
    assert hyperedge_name == 'e1'

    # Test that all hyperedge attributes are correct
    assert H._hyperedge_attributes[hyperedge_name]['tail'] == tail
    assert H._hyperedge_attributes[hyperedge_name]['head'] == head
    assert H._hyperedge_attributes[hyperedge_name]['weight'] == 5
    assert H._hyperedge_attributes[hyperedge_name]['color'] == 'black'

    # Test that successor list contains the correct info
    assert frozen_head in H._successors[frozen_tail]
    assert hyperedge_name in H._successors[frozen_tail][frozen_head]

    # Test that the precessor list contains the correct info
    assert frozen_tail in H._predecessors[frozen_head]
    assert hyperedge_name in H._predecessors[frozen_head][frozen_tail]

    # Test that forward-stars and backward-stars contain the correct info
    for node in frozen_tail:
        assert hyperedge_name in H._forward_star[node]
    for node in frozen_head:
        assert hyperedge_name in H._backward_star[node]

    # Test that adding same hyperedge will only update attributes
    new_attrib = {'weight': 10}
    H.add_hyperedge(tail, head, attr_dict=new_attrib)
    assert H._hyperedge_attributes[hyperedge_name]['weight'] == 10
    assert H._hyperedge_attributes[hyperedge_name]['color'] == 'black'

    try:
        H.add_hyperedge(set(), set())
        assert False
    except ValueError:
        pass
    except BaseException as e:
        assert False, e