from lpsolve55 import *

def test_lp_solve():
	# Set up an lp for the following:
	# min: x1 + x2;
	# c1: x1 >= 1;
	# x2 >= 1;
	# x1 + x2 >= 2;
	# int x1;
	lp = lpsolve('make_lp', 0, 2)
	lpsolve('set_obj_fn', lp, [1, 1])
	lpsolve('add_constraint', lp, [1, 0], GE, 1)
	lpsolve('add_constraint', lp, [1, 1], GE, 2)
	lpsolve('set_lowbo', lp, 2, 1)
	lpsolve('set_int',lp, 1, True)
	lpsolve('solve', lp)
	# The solution should be x1 = 1, x2 = 1
	assert(lpsolve('get_variables', lp)[0] == [1.0, 1.0])
	lpsolve('delete_lp', lp)
