import os

from halp.signaling_hypergraph import SignalingHypergraph

EPSILON=0.0001
CONSTANT=1000000

######################################
## Objective Function:
######################################
def write_objective(H, out):
    out.write('min: ')
    # Minimize Sum of Active Edges
    for e in H.get_hyperedge_id_set():
        out.write(' + %d %s' % (H.get_hyperedge_weight(e),e))
    out.write(';\n')
    return out

######################################
## Activity Variable Constraints
######################################
def write_activity_variable_constraints(H, src, out, c):
    ######################################
    ## Active Edges: Constraint for each of T(e),H(e)
    for e in H.get_hyperedge_id_set():
        Pr_e = H.get_hyperedge_pos_regs(e)
        T_e = H.get_hyperedge_tail(e)
        if len(T_e) + len(Pr_e) > 0:
            ## format: \sum_{v \in T(e)} \alpha_v >= |T(e)| \alpha_e
            ##       = \sum_{v \in T(e)} \alpha_v - |T(e)| \alpha_e >= 0
            out.write('hyperedge_tails_%s_c%d:' % (e,c))
            for v in T_e:
                out.write(' + a_%s' % (v))
            for v in Pr_e:
                out.write(' + a_%s' % (v))
            out.write(' - %d %s >= 0;\n' % (len(T_e) + len(Pr_e),e))
            c+=1 #increment constraint counter
        H_e = H.get_hyperedge_head(e)
        if len(H_e) > 0:
            ## format: \sum_{v \in H(e)} \alpha_v >= |H(e)| \alpha_e
            ##       = \sum_{v \in H(e)} \alpha_v - |H(e)| \alpha_e >= 0
            out.write('hyperedge_heads_%s_c%d:' % (e,c))
            for v in H_e:
                out.write(' + a_%s' % (v))
            out.write(' - %d %s >= 0;\n' % (len(H_e),e))
            c+=1 #increment constraint counter        

    ######################################
    ## Incoming Edges: at least one edge in BS(v) must be active 
    ## (except for hypernodes containing src)
    for node in H.get_hypernode_set(): 
        ## don't write constraint for any hypernode containing src node.
        if src == node:
            continue
        ## get backwards star:
        bstar = H.get_backward_star(node)
        if len(bstar)==0:
            ## format if empty bstar: \alpha_v = 0
            # print 'WARNING: hnode %s has an empty backward-star. Alpha var must be 0.' % (node)
            out.write('incoming_%s_c%d: a_%s = 0;\n' % (node,c,node))
        else:
            ## format for non-empty bstar: 
            ##   \sum_{e \in BS(v)} \alpha_e >= \alpha_v
            ## = \sum_{e \in BS(v)} \alpha_e - \alpha_v >= 0
            out.write('incoming_%s_c%d:' % (node,c))
            for e in bstar:
                out.write(' + %s' % (e))
            out.write(' - a_%s >= 0;\n' % (node))    
        c+=1 #increment constraint counter
    return out, c

######################################
## Fixed Value Constraints
######################################
def write_fixed_value_constraints(H, tofix, out, c):
    # requre that at least one hypernode containing t is active.
    ## tofix is a dictionary of {hypernode: <0 or 1>}
    for t in tofix:
        out.write('fixed_%s_c%d: a_%s = %d;\n' % (t,c,t,tofix[t]))  
        c+=1 #increment constraint counter
    return out,c

######################################
## Order Variable Constraints
######################################
def write_order_variable_constraints(H, out, c):
    ######################################
    ## Order Bounds: 0 <= o_v <= \alpha_v \forall v \in V
    for hypernode in H.get_hypernode_set():
        name = 'a_%s' % (hypernode)
        ## format: o_v >= 0
        out.write('order_lb_%s_c%d: o_%s >= 0;\n' % (name,c,name))
        c+=1 #increment constraint counter

        ## format: o_v - \alpha_v <= 0
        out.write('order_ub_%s_%d: o_%s - %s <= 0;\n' % (name,c,name,name))
        c+=1 #increment constraint counter

    ######################################
    ## Order Constraints: o_u <= o_v - \epsilon + C (1-\alpha_e) \forall u,v in (T(e),H(e)) \forall e \in E 
    for e in H.get_hyperedge_id_set(): 
        ename = e
        for u in (H.get_hyperedge_tail(e).union(H.get_hyperedge_pos_regs(e))):
            uname = 'a_%s' % (u)
            for v in H.get_hyperedge_head(e):
                vname = 'a_%s' % (v)
                ## format: o_u <= o_v - \epsilon + C (1-\alpha_e) 
                ##       = o_u - o_v + C \alpha_e <= C - \epsilon
                out.write('order_%s_c%d: o_%s - o_%s + %d %s <= %f;\n' % \
                              (ename,c,uname,vname,CONSTANT,ename,CONSTANT-EPSILON))
                c+=1 #increment constraint counter       
    return out,c

######################################
## Activity Variable Types
######################################
def write_activity_variable_types(H, out):
    # for hnode in H.getHypernodes():
    #     s += (' a_%s\n' % (hnode))
    for node in H.get_hypernode_set():
        out.write('bin a_%s;\n' % (node))
    for e in H.get_hyperedge_id_set():
        out.write('bin %s;\n' % (e))
    return out

################################
## Cleanup
################################
def clear_lp(outprefix):
    os.system('rm -f %s.lp' % (outprefix))