from sage.rings.polynomial.polydict cimport ETuple
from sage.rings.polynomial.multi_polynomial_libsingular cimport MPolynomial_libsingular, MPolynomialRing_libsingular


cpdef tuple poly_to_tup(MPolynomial_libsingular poly)
cpdef MPolynomial_libsingular tup_to_poly(tuple eq_tup, MPolynomialRing_libsingular parent)
cpdef tuple resize(tuple eq_tup, dict idx_map, int nvars)
cpdef ETuple get_variables_degrees(list eqns)
cpdef list variables(tuple eq_tup)
cpdef constant_coeff(tuple eq_tup)
cpdef tuple apply_coeff_map(tuple eq_tup, coeff_map)
cpdef bint tup_fixes_sq(tuple eq_tup)
cpdef dict subs_squares(dict eq_dict, dict known_sq)
cdef tuple to_monic(dict eq_dict)
cdef tuple reduce_poly_dict(dict eq_dict, ETuple nonz, dict known_sq)
cpdef dict compute_known_powers(ETuple max_deg, dict val_dict)
cpdef dict subs(tuple poly_tup, dict known_powers)
cpdef int poly_tup_cmp(tuple tleft, tuple tright)

cdef tuple tup_mul(tuple p1, tuple p2)
cdef dict remove_gcf(dict eq_dict, ETuple nonz)
