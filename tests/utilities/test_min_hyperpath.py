def test_min_hyperpath():
    from halp.signaling_hypergraph import SignalingHypergraph
    from halp.utilities import min_hyperpath as mh
    from lpsolve55 import *

    H = SignalingHypergraph()
    H.read("tests/data/basic_signaling_hypergraph.txt")
    out = open('MILP.lp','w')
    out = mh.write_objective(H,out)
    out, c = mh.write_activity_variable_constraints(H, "s", out, 0)
    out, c = mh.write_fixed_value_constraints(H, {"t":1}, out, c)
    out, c = mh.write_order_variable_constraints(H, out, c)
    out = mh.write_activity_variable_types(H, out)
    out.close()

    lp = lpsolve('read_LP', 'MILP.lp')
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('solve', lp)
    lpsolve('set_verbose', lp, IMPORTANT)

    V = lpsolve('get_variables', lp)[0]
    lpsolve('delete_lp', lp)
    mh.clear_lp('MILP')

    min_path = set()
    i = 0
    for e in H.get_hyperedge_id_set():
        if V[i] == 1:
            min_path.add((frozenset(H.get_hyperedge_tail(e)),frozenset(H.get_hyperedge_head(e))))
        i += 1
    expected_min_path = set()
    expected_min_path.add((frozenset(['s']),frozenset(['x','y'])))
    expected_min_path.add((frozenset(['s']),frozenset(['z'])))
    expected_min_path.add((frozenset(['x','y','z']),frozenset(['u','t'])))

    assert min_path.difference(expected_min_path) == set()
    assert expected_min_path.difference(min_path) == set()
