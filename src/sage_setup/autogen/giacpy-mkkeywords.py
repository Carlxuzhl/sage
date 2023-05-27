# see the discussion in  trac #29171 about where to store this file.
"""
This file is to help the maintainer to upgrade the giac keywords in

     giacpy or giacpy_sage or sage.libs.giac

It creates auto-methods.pxi, keywords.pxi, newkeyword.pxi
It needs:

- the ``cas_help`` program from a giac installation
- the ``aide_cas.txt`` file that you can built yourself like this::

    grep -E '^#' share/giac/doc/aide_cas  |sed -e 's/^# //' >aide_cas.txt

It should not be used on the fly for an automatic installation script, because auto-methods.pxi is
quite long to be built and adding new giac keywords often break the built of giacpy
while not implementing a new giac keyword doesn't break the giacpy built.

newkeywords.pxi is just created to check things manually but is not used in iacpy or sage.libs.giac

AUTHORS:

- Frederic Han (2020-07)
"""
from subprocess import PIPE, Popen

blacklist = ['eval', 'cas_setup', 'i', 'list', 'input', 'in', 'sto', 'string', 'and', 'break', 'continue', 'else', 'for', 'from', 'if', 'not', 'or', 'pow', 'print', 'return', 'set[]', 'try', 'while', 'open', 'output', 'do', 'of', 'Request', 'i[]', '[]', 'ffunction', 'sleep', '[..]']

toremove = ['!', '!=', '#', '$', '%', '/%', '%/', '%{%}', '&&', '&*', '&^', "'", '()', '*', '*=', '+', '-', '+&', '+=', '+infinity', '-<', '-=', '->', '-infinity', '.*', '.+', '.-', './', '.^', '/=', ':=', '<', '<=', '=', '=<', '==', '=>', '>', '>=', '?', '@', '@@', 'ACOSH', 'ACOT', 'ACSC', 'ASEC', 'ASIN', 'ASINH', 'ATAN', 'ATANH', 'COND', 'COS', 'COSH', 'COT', 'CSC', 'CST', 'Celsius2Fahrenheit', 'ClrDraw', 'ClrGraph', 'ClrIO', 'CyclePic', 'DIGITS', 'DOM_COMPLEX', 'DOM_FLOAT', 'DOM_FUNC', 'DOM_IDENT', 'DOM_INT', 'DOM_LIST', 'DOM_RAT', 'DOM_STRING', 'DOM_SYMBOLIC', 'DOM_int', 'DelFold', 'DelVar', 'Det', 'Dialog', 'Digits', 'Disp', 'DispG', 'DispHome', 'DrawFunc', 'DrawInv', 'DrawParm', 'DrawPol', 'DrawSlp', 'DropDown', 'DrwCtour', 'ERROR', 'EXP', 'EndDlog', 'FALSE', 'False', 'Fahrenheit2Celsius', 'Fill', 'Gcd', 'GetFold', 'Graph', 'IFTE', 'Input', 'InputStr', 'Int', 'Inverse', 'LN', 'LQ', 'LSQ', 'NORMALD', 'NewFold', 'NewPic', 'Nullspace', 'Output', 'Ox_2d_unit_vector', 'Ox_3d_unit_vector', 'Oy_2d_unit_vector', 'Oy_3d_unit_vector', 'Oz_3d_unit_vector', 'Pause', 'PopUp', 'Quo', 'REDIM', 'REPLACE', 'RclPic', 'Rem', 'Resultant', 'RplcPic', 'Rref', 'SCALE', 'SCALEADD', 'SCHUR', 'SIN', 'SVD', 'SVL', 'SWAPCOL', 'SWAPROW', 'SetFold', 'Si', 'StoPic', 'Store', 'TAN', 'TRUE', 'True', 'TeX', 'Text', 'Title', 'Unarchiv', 'WAIT', '^', '_(cm/s)', '_(ft/s)', '_(ft*lb)', '_(m/s)', '_(m/s^2)', '_(rad/s)', '_(rad/s^2)', '_(tr/min)', '_(tr/s)', '_A', '_Angstrom', '_Bq', '_Btu', '_Ci', '_F', '_F_', '_Fdy', '_G_', '_Gal', '_Gy', '_H', '_Hz', '_I0_', '_J', '_K', '_Kcal', '_MHz', '_MW', '_MeV', '_N', '_NA_', '_Ohm', '_P', '_PSun_', '_Pa', '_R', '_REarth_', '_RSun_', '_R_', '_Rankine', '_Rinfinity_', '_S', '_St', '_StdP_', '_StdT_', '_Sv', '_T', '_V', '_Vm_', '_W', '_Wb', '_Wh', '_a', '_a0_', '_acre', '_alpha_', '_angl_', '_arcmin', '_arcs', '_atm', '_au', '_b', '_bar', '_bbl', '_bblep', '_bu', '_buUS', '_c3_', '_c_', '_cal', '_cd', '_chain', '_cm', '_cm^2', '_cm^3', '_ct', '_cu', '_d', '_dB', '_deg', '_degreeF', '_dyn', '_eV', '_epsilon0_', '_epsilon0q_', '_epsilonox_', '_epsilonsi_', '_erg', '_f0_', '_fath', '_fbm', '_fc', '_fermi', '_flam', '_fm', '_ft', '_ft*lb', '_ftUS', '_ft^2', '_ft^3', '_g', '_g_', '_ga', '_galC', '_galUK', '_galUS', '_gf', '_gmol', '_gon', '_grad', '_grain', '_h', '_h_', '_ha', '_hbar_', '_hp', '_in', '_inH20', '_inHg', '_in^2', '_in^3', '_j', '_kWh', '_k_', '_kg', '_kip', '_km', '_km^2', '_knot', '_kph', '_kq_', '_l', '_lam', '_lambda0_', '_lambdac_', '_lb', '_lbf', '_lbmol', '_lbt', '_lep', '_liqpt', '_lm', '_lx', '_lyr', '_m', '_mEarth_', '_m^2', '_m^3', '_me_', '_mho', '_miUS', '_miUS^2', '_mi^2', '_mil', '_mile', '_mille', '_ml', '_mm', '_mmHg', '_mn', '_mol', '_mp_', '_mph', '_mpme_', '_mu0_', '_muB_', '_muN_', '_oz', '_ozUK', '_ozfl', '_ozt', '_pc', '_pdl', '_ph', '_phi_', '_pk', '_psi', '_ptUK', '_q_', '_qe_', '_qepsilon0_', '_qme_', '_qt', '_rad', '_rad_', '_rd', '_rem', '_rod', '_rpm', '_s', '_sb', '_sd_', '_sigma_', '_slug', '_sr', '_st', '_syr_', '_t', '_tbsp', '_tec', '_tep', '_tex', '_therm', '_ton', '_tonUK', '_torr', '_tr', '_tsp', '_twopi_', '_u', '_yd', '_yd^2', '_yd^3', '_yr', '_\xc2\xb5', '_µ', 'assert', 'affichage', 'alors', 'animate', 'animate3d', 'animation', 'approx_mode', 'archive', 'args', 'as_function_of', 'asc', 'asec', 'assign', 'backquote', 'begin', 'black', 'blanc', 'bleu', 'bloc', 'blue', 'breakpoint', 'by', 'c1oc2', 'c1op2', 'cache_tortue', 'cap', 'cap_flat_line', 'cap_round_line', 'cap_square_line', 'case', 'cat', 'catch', 'cd', 'choosebox', 'click', 'close', 'complex_mode', 'de', 'del', 'debug', 'default', 'div', 'double', 'ecris', 'efface', 'elif', 'end', 'end_for', 'end_if', 'end_while', 'epaisseur', 'epaisseur_ligne_1', 'epaisseur_ligne_2', 'epaisseur_ligne_3', 'epaisseur_ligne_4', 'epaisseur_ligne_5', 'epaisseur_ligne_6', 'epaisseur_ligne_7', 'epaisseur_point_1', 'epaisseur_point_2', 'epaisseur_point_3', 'epaisseur_point_4', 'epaisseur_point_5', 'epaisseur_point_6', 'epaisseur_point_7', 'erase', 'erase3d', 'est_cocyclique', 'est_inclus', 'et', 'faire', 'faux', 'feuille', 'ffaire', 'ffonction', 'fi', 'filled', 'fin_enregistrement', 'float', 'fonction', 'fopen', 'format', 'fpour', 'frame_3d', 'frames', 'fsi', 'ftantque', 'func', 'function', 'gauche', 'gl_ortho', 'gl_quaternion', 'gl_rotation', 'gl_shownames', 'gl_texture', 'gl_x', 'gl_x_axis_color', 'gl_x_axis_name', 'gl_x_axis_unit', 'gl_xtick', 'gl_y', 'gl_y_axis_color', 'gl_y_axis_name', 'gl_y_axis_unit', 'gl_ytick', 'gl_z', 'gl_z_axis_color', 'gl_z_axis_name', 'gl_z_axis_unit', 'gl_ztick', 'gnuplot', 'goto', 'graph2tex', 'graph3d2tex', 'graphe', 'graphe3d', 'graphe_probabiliste', 'graphe_suite', 'green', 'grid_paper', 'hidden_name', 'identifier', 'ifft', 'ifte', 'inputform', 'intersect', 'is_included', 'jusqu_a', 'jusqua', 'jusque', 'keep_algext', 'kill', 'label', 'labels', 'len', 'leve_crayon', 'line_width_1', 'line_width_2', 'line_width_3', 'line_width_4', 'line_width_5', 'line_width_6', 'line_width_7', 'lis', 'local', 'minus', 'mod', 'noir', 'nom_cache', 'non', 'od', 'option', 'otherwise', 'ou', 'pas', 'point_arret', 'point_carre', 'point_croix', 'point_div', 'point_etoile', 'point_invisible', 'point_losange', 'point_milieu', 'point_plus', 'point_point', 'point_polaire', 'point_triangle', 'point_width_1', 'point_width_2', 'point_width_3', 'point_width_4', 'point_width_5', 'point_width_6', 'point_width_7', 'pour', 'proc', 'program', 'quadrant1', 'quadrant2', 'quadrant3', 'quadrant4', 'range', 'redim', 'repeat', 'repete', 'repeter', 'replace', 'restart', 'rouge', 'saisir', 'saisir_chaine', 'sauve', 'save_history', 'scale', 'scaleadd', 'si', 'sinon', 'size', 'stack', 'step', 'switch', 'tantque', 'test', 'textinput', 'then', 'thiele', 'time', 'to', 'union', 'until', 'var', 'vector', 'vers', 'vert', 'vrai', 'watch', 'when', 'white', 'with_sqrt', 'write', 'wz_certificate', 'xor', 'yellow', '{}', '|', '||','expression']


# basekeywords=['sin', 'cos', 'exp', 'tan', 'solve']


# usualvars=['x','y','z','t','u','v']

moremethods=['type','zip']
# append seems fixed with current giac.


# the file aide_cas.txt should contain one line by keywords+ its synonyms. You can create it from th file aide_cas
# provided in giac source archive or installled in share/giac/doc like this:
#grep -E '^#' share/giac/doc/aide_cas  |sed -e 's/^# //' >aide_cas.txt
with open('aide_cas.txt') as f:
    mostkeywords=f.read().split()

mostkeywordorig=['Airy_Ai', 'Airy_Bi', 'Archive', 'BesselJ', 'BesselY', 'Beta', 'BlockDiagonal', 'Ci', 'Circle', 'Col', 'CopyVar', 'Dirac', 'Ei', 'Factor', 'GF', 'Gamma', 'Heaviside', 'JordanBlock', 'LU', 'LambertW', 'Li', 'Line', 'LineHorz', 'LineTan', 'LineVert', 'Phi', 'Pi', 'Psi', 'QR', 'RandSeed', 'Row', 'SortA', 'SortD', 'UTPC', 'UTPF', 'UTPN', 'UTPT', 'VARS', 'VAS', 'VAS_positive', 'Zeta', '_qe_', 'a2q', 'abcuv', 'about', 'abs', 'abscissa', 'accumulate_head_tail', 'acos', 'acos2asin', 'acos2atan', 'acosh', 'acot', 'acsc', 'acyclic', 'add', 'add_arc', 'add_edge', 'add_vertex', 'additionally', 'adjacency_matrix', 'adjoint_matrix', 'affix', 'algsubs', 'algvar', 'all_trig_solutions', 'allpairs_distance', 'alog10', 'altitude', 'angle', 'angle_radian', 'angleat', 'angleatraw', 'ans', 'antiprism_graph', 'apply', 'approx', 'arc', 'arcLen', 'arccos', 'arccosh', 'arclen', 'arcsin', 'arcsinh', 'arctan', 'arctanh', 'area', 'areaat', 'areaatraw', 'areaplot', 'arg', 'array', 'arrivals', 'articulation_points', 'asin', 'asin2acos', 'asin2atan', 'asinh', 'assign_edge_weights', 'assume', 'at', 'atan', 'atan2acos', 'atan2asin', 'atanh', 'atrig2ln', 'augment', 'auto_correlation', 'autosimplify', 'avance', 'avgRC', 'axes', 'back', 'backward', 'baisse_crayon', 'bandwidth', 'bar_plot', 'bartlett_hann_window', 'barycenter', 'base', 'basis', 'batons', 'bellman_ford', 'bernoulli', 'besselJ', 'besselY', 'betad', 'betad_cdf', 'betad_icdf', 'betavariate', 'bezier', 'bezout_entiers', 'biconnected_components', 'binomial', 'binomial_cdf', 'binomial_icdf', 'bins', 'bipartite', 'bipartite_matching', 'bisection_solver', 'bisector', 'bit_depth', 'bitand', 'bitor', 'bitxor', 'blackman_harris_window', 'blackman_window', 'blockmatrix', 'bohman_window', 'border', 'boxwhisker', 'brent_solver', 'bvpsolve', 'cFactor', 'cSolve', 'cZeros', 'camembert', 'canonical_form', 'canonical_labeling', 'cartesian_product', 'cauchy', 'cauchy_cdf', 'cauchy_icdf', 'cauchyd', 'cauchyd_cdf', 'cauchyd_icdf', 'cdf', 'ceil', 'ceiling', 'center', 'center2interval', 'centered_cube', 'centered_tetrahedron', 'cfactor', 'cfsolve', 'changebase', 'channel_data', 'channels', 'char', 'charpoly', 'chinrem', 'chisquare', 'chisquare_cdf', 'chisquare_icdf', 'chisquared', 'chisquared_cdf', 'chisquared_icdf', 'chisquaret', 'choice', 'cholesky', 'chr', 'chrem', 'chromatic_index', 'chromatic_number', 'chromatic_polynomial', 'circle', 'circumcircle', 'classes', 'clear', 'clique_cover', 'clique_cover_number', 'clique_number', 'clique_stats', 'clustering_coefficient', 'coeff', 'coeffs', 'col', 'colDim', 'colNorm', 'colSwap', 'coldim', 'collect', 'colnorm', 'color', 'colspace', 'colswap', 'comDenom', 'comb', 'combine', 'comment', 'common_perpendicular', 'companion', 'compare', 'complete_binary_tree', 'complete_graph', 'complete_kary_tree', 'complex', 'complex_variables', 'complexroot', 'concat', 'cond', 'condensation', 'cone', 'confrac', 'conic', 'conj', 'conjugate_equation', 'conjugate_gradient', 'connected', 'connected_components', 'cont', 'contains', 'content', 'contourplot', 'contract_edge', 'convert', 'convertir', 'convex', 'convexhull', 'convolution', 'coordinates', 'copy', 'correlation', 'cos', 'cos2sintan', 'cosh', 'cosine_window', 'cot', 'cote', 'count', 'count_eq', 'count_inf', 'count_sup', 'courbe_parametrique', 'courbe_polaire', 'covariance', 'covariance_correlation', 'cpartfrac', 'crationalroot', 'crayon', 'createwav', 'cross', 'crossP', 'cross_correlation', 'cross_point', 'cross_ratio', 'crossproduct', 'csc', 'csolve', 'csv2gen', 'cube', 'cumSum', 'cumsum', 'cumulated_frequencies', 'curl', 'current_sheet', 'curvature', 'curve', 'cyan', 'cycle2perm', 'cycle_graph', 'cycleinv', 'cycles2permu', 'cyclotomic', 'cylinder', 'dash_line', 'dashdot_line', 'dashdotdot_line', 'dayofweek', 'deSolve', 'debut_enregistrement', 'degree', 'degree_sequence', 'delcols', 'delete_arc', 'delete_edge', 'delete_vertex', 'delrows', 'deltalist', 'denom', 'densityplot', 'departures', 'derive', 'deriver', 'desolve', 'dessine_tortue', 'det', 'det_minor', 'developper', 'developper_transcendant', 'dfc', 'dfc2f', 'diag', 'diff', 'digraph', 'dijkstra', 'dim', 'directed', 'discard_edge_attribute', 'discard_graph_attribute', 'discard_vertex_attribute', 'disjoint_union', 'display', 'disque', 'disque_centre', 'distance', 'distance2', 'distanceat', 'distanceatraw', 'divergence', 'divide', 'divis', 'division_point', 'divisors', 'divmod', 'divpc', 'dnewton_solver', 'dodecahedron', 'domain', 'dot', 'dotP', 'dot_paper', 'dotprod', 'draw_arc', 'draw_circle', 'draw_graph', 'draw_line', 'draw_pixel', 'draw_polygon', 'draw_rectangle', 'droit', 'droite_tangente', 'dsolve', 'duration', 'e', 'e2r', 'ecart_type', 'ecart_type_population', 'ecm_factor', 'edge_connectivity', 'edges', 'egcd', 'egv', 'egvl', 'eigVc', 'eigVl', 'eigenvals', 'eigenvalues', 'eigenvectors', 'eigenvects', 'element', 'eliminate', 'ellipse', 'entry', 'envelope', 'epsilon', 'epsilon2zero', 'equal', 'equal2diff', 'equal2list', 'equation', 'equilateral_triangle', 'erf', 'erfc', 'error', 'est_permu', 'euler', 'euler_gamma', 'euler_lagrange', 'eval_level', 'evala', 'evalb', 'evalc', 'evalf', 'evalm', 'even', 'evolute', 'exact', 'exbisector', 'excircle', 'execute', 'exp', 'exp2list', 'exp2pow', 'exp2trig', 'expand', 'expexpand', 'expln', 'exponential', 'exponential_cdf', 'exponential_icdf', 'exponential_regression', 'exponential_regression_plot', 'exponentiald', 'exponentiald_cdf', 'exponentiald_icdf', 'export_graph', 'expovariate', 'expr', 'extend', 'extract_measure', 'extrema', 'ezgcd', 'f2nd', 'fMax', 'fMin', 'fPart', 'faces', 'facteurs_premiers', 'factor', 'factor_xn', 'factorial', 'factoriser', 'factoriser_entier', 'factoriser_sur_C', 'factors', 'fadeev', 'false', 'falsepos_solver', 'fclose', 'fcoeff', 'fdistrib', 'fft', 'fieldplot', 'find', 'find_cycles', 'findhelp', 'fisher', 'fisher_cdf', 'fisher_icdf', 'fisherd', 'fisherd_cdf', 'fisherd_icdf', 'fitdistr', 'flatten', 'float2rational', 'floor', 'flow_polynomial', 'fmod', 'foldl', 'foldr', 'fonction_derivee', 'forward', 'fourier_an', 'fourier_bn', 'fourier_cn', 'fprint', 'frac', 'fracmod', 'frame_2d', 'frequencies', 'frobenius_norm', 'froot', 'fsolve', 'fullparfrac', 'funcplot', 'function_diff', 'fxnd', 'gammad', 'gammad_cdf', 'gammad_icdf', 'gammavariate', 'gauss', 'gauss15', 'gauss_seidel_linsolve', 'gaussian_window', 'gaussjord', 'gaussquad', 'gbasis', 'gbasis_max_pairs', 'gbasis_reinject', 'gbasis_simult_primes', 'gcd', 'gcdex', 'genpoly', 'geometric', 'geometric_cdf', 'geometric_icdf', 'getDenom', 'getKey', 'getNum', 'getType', 'get_edge_attribute', 'get_edge_weight', 'get_graph_attribute', 'get_vertex_attribute', 'girth', 'gl_showaxes', 'grad', 'gramschmidt', 'graph', 'graph_automorphisms', 'graph_charpoly', 'graph_complement', 'graph_diameter', 'graph_equal', 'graph_join', 'graph_power', 'graph_rank', 'graph_spectrum', 'graph_union', 'graph_vertices', 'greduce', 'greedy_color', 'grid_graph', 'groupermu', 'hadamard', 'half_cone', 'half_line', 'halftan', 'halftan_hyp2exp', 'halt', 'hamdist', 'hamming_window', 'hann_poisson_window', 'hann_window', 'harmonic_conjugate', 'harmonic_division', 'has', 'has_arc', 'has_edge', 'hasard', 'head', 'heading', 'heapify', 'heappop', 'heappush', 'hermite', 'hessenberg', 'hessian', 'heugcd', 'hexagon', 'highlight_edges', 'highlight_subgraph', 'highlight_trail', 'highlight_vertex', 'highpass', 'hilbert', 'histogram', 'hold', 'homothety', 'horner', 'hybrid_solver', 'hybridj_solver', 'hybrids_solver', 'hybridsj_solver', 'hyp2exp', 'hyperbola', 'hypercube_graph', 'iPart', 'iabcuv', 'ibasis', 'ibpdv', 'ibpu', 'icdf', 'ichinrem', 'ichrem', 'icomp', 'icontent', 'icosahedron', 'id', 'identity', 'idivis', 'idn', 'iegcd', 'ifactor', 'ifactors', 'igamma', 'igcd', 'igcdex', 'ihermite', 'ilaplace', 'im', 'imag', 'image', 'implicitdiff', 'implicitplot', 'import_graph', 'inString', 'in_ideal', 'incidence_matrix', 'incident_edges', 'incircle', 'increasing_power', 'independence_number', 'indets', 'index', 'induced_subgraph', 'inequationplot', 'inf', 'infinity', 'insert', 'insmod', 'int', 'intDiv', 'integer', 'integrate', 'integrer', 'inter', 'interactive_odeplot', 'interactive_plotode', 'interp', 'interval', 'interval2center', 'interval_graph', 'inv', 'inverse', 'inversion', 'invisible_point', 'invlaplace', 'invztrans', 'iquo', 'iquorem', 'iratrecon', 'irem', 'isPrime', 'is_acyclic', 'is_arborescence', 'is_biconnected', 'is_bipartite', 'is_clique', 'is_collinear', 'is_concyclic', 'is_conjugate', 'is_connected', 'is_coplanar', 'is_cospherical', 'is_cut_set', 'is_cycle', 'is_directed', 'is_element', 'is_equilateral', 'is_eulerian', 'is_forest', 'is_graphic_sequence', 'is_hamiltonian', 'is_harmonic', 'is_harmonic_circle_bundle', 'is_harmonic_line_bundle', 'is_inside', 'is_integer_graph', 'is_isomorphic', 'is_isosceles', 'is_network', 'is_orthogonal', 'is_parallel', 'is_parallelogram', 'is_permu', 'is_perpendicular', 'is_planar', 'is_prime', 'is_pseudoprime', 'is_rectangle', 'is_regular', 'is_rhombus', 'is_square', 'is_strongly_connected', 'is_strongly_regular', 'is_tournament', 'is_tree', 'is_triconnected', 'is_two_edge_connected', 'is_vertex_colorable', 'is_weighted', 'ismith', 'isobarycenter', 'isom', 'isomorphic_copy', 'isopolygon', 'isosceles_triangle', 'isprime', 'ithprime', 'jacobi_equation', 'jacobi_linsolve', 'jacobi_symbol', 'jordan', 'kde', 'keep_pivot', 'ker', 'kernel', 'kernel_density', 'kneser_graph', 'kolmogorovd', 'kolmogorovt', 'kovacicsols', 'kspaths', 'l1norm', 'l2norm', 'lagrange', 'laguerre', 'laplace', 'laplacian', 'laplacian_matrix', 'latex', 'lcf_graph', 'lcm', 'lcoeff', 'ldegree', 'left', 'left_rectangle', 'legend', 'legendre', 'legendre_symbol', 'length', 'lgcd', 'lhs', 'ligne_chapeau_carre', 'ligne_chapeau_plat', 'ligne_chapeau_rond', 'ligne_polygonale', 'ligne_polygonale_pointee', 'ligne_tiret', 'ligne_tiret_point', 'ligne_tiret_pointpoint', 'ligne_trait_plein', 'limit', 'limite', 'lin', 'line', 'line_graph', 'line_inter', 'line_paper', 'line_segments', 'linear_interpolate', 'linear_regression', 'linear_regression_plot', 'lineariser', 'lineariser_trigo', 'linfnorm', 'linsolve', 'linspace', 'lis_phrase', 'list2exp', 'list2mat', 'list_edge_attributes', 'list_graph_attributes', 'list_vertex_attributes', 'listplot', 'lll', 'ln', 'lname', 'lncollect', 'lnexpand', 'locus', 'log', 'log10', 'logarithmic_regression', 'logarithmic_regression_plot', 'logb', 'logistic_regression', 'logistic_regression_plot', 'lower', 'lowest_common_ancestor', 'lowpass', 'lp_assume', 'lp_bestprojection', 'lp_binary', 'lp_binaryvariables', 'lp_breadthfirst', 'lp_depthfirst', 'lp_depthlimit', 'lp_firstfractional', 'lp_gaptolerance', 'lp_hybrid', 'lp_initialpoint', 'lp_integer', 'lp_integertolerance', 'lp_integervariables', 'lp_interiorpoint', 'lp_iterationlimit', 'lp_lastfractional', 'lp_maxcuts', 'lp_maximize', 'lp_method', 'lp_mostfractional', 'lp_nodelimit', 'lp_nodeselect', 'lp_nonnegative', 'lp_nonnegint', 'lp_pseudocost', 'lp_simplex', 'lp_timelimit', 'lp_variables', 'lp_varselect', 'lp_verbose', 'lpsolve', 'lsmod', 'lsq', 'lu', 'lvar', 'mRow', 'mRowAdd', 'magenta', 'make_directed', 'make_weighted', 'makelist', 'makemat', 'makesuite', 'makevector', 'map', 'maple2mupad', 'maple2xcas', 'maple_ifactors', 'maple_mode', 'markov', 'mat2list', 'mathml', 'matpow', 'matrix', 'matrix_norm', 'max', 'maxflow', 'maximal_independent_set', 'maximize', 'maximum_clique', 'maximum_degree', 'maximum_independent_set', 'maximum_matching', 'maxnorm', 'mean', 'median', 'median_line', 'member', 'mgf', 'mid', 'middle_point', 'midpoint', 'min', 'minimal_edge_coloring', 'minimal_spanning_tree', 'minimal_vertex_coloring', 'minimax', 'minimize', 'minimum_cut', 'minimum_degree', 'mkisom', 'mksa', 'modgcd', 'mods', 'monotonic', 'montre_tortue', 'moustache', 'moving_average', 'moyal', 'moyenne', 'mul', 'mult_c_conjugate', 'mult_conjugate', 'multinomial', 'multiplier_conjugue', 'multiplier_conjugue_complexe', 'multiply', 'mupad2maple', 'mupad2xcas', 'mycielski', 'nCr', 'nDeriv', 'nInt', 'nPr', 'nSolve', 'ncols', 'negbinomial', 'negbinomial_cdf', 'negbinomial_icdf', 'neighbors', 'network_transitivity', 'newList', 'newMat', 'newton', 'newton_solver', 'newtonj_solver', 'nextperm', 'nextprime', 'nlpsolve', 'nodisp', 'non_recursive_normal', 'nop', 'nops', 'norm', 'normal', 'normal_cdf', 'normal_icdf', 'normald', 'normald_cdf', 'normald_icdf', 'normalize', 'normalt', 'normalvariate', 'nprimes', 'nrows', 'nuage_points', 'nullspace', 'number_of_edges', 'number_of_spanning_trees', 'number_of_triangles', 'number_of_vertices', 'numer', 'octahedron', 'odd', 'odd_girth', 'odd_graph', 'odeplot', 'odesolve', 'op', 'open_polygon', 'ord', 'order', 'order_size', 'ordinate', 'orthocenter', 'orthogonal', 'osculating_circle', 'p1oc2', 'p1op2', 'pa2b2', 'pade', 'parabola', 'parallel', 'parallelepiped', 'parallelogram', 'parameq', 'parameter', 'paramplot', 'parfrac', 'pari', 'part', 'partfrac', 'parzen_window', 'pas_de_cote', 'path_graph', 'pcar', 'pcar_hessenberg', 'pcoef', 'pcoeff', 'pencolor', 'pendown', 'penup', 'perimeter', 'perimeterat', 'perimeteratraw', 'periodic', 'perm', 'perminv', 'permu2cycles', 'permu2mat', 'permuorder', 'permute_vertices', 'perpen_bisector', 'perpendicular', 'petersen_graph', 'peval', 'pi', 'piecewise', 'pivot', 'pixoff', 'pixon', 'planar', 'plane', 'plane_dual', 'playsnd', 'plex', 'plot', 'plot3d', 'plotarea', 'plotcdf', 'plotcontour', 'plotdensity', 'plotfield', 'plotfunc', 'plotimplicit', 'plotinequation', 'plotlist', 'plotode', 'plotparam', 'plotpolar', 'plotproba', 'plotseq', 'plotspectrum', 'plotwav', 'plus_point', 'pmin', 'point', 'point2d', 'point3d', 'poisson', 'poisson_cdf', 'poisson_icdf', 'poisson_window', 'polar', 'polar_coordinates', 'polar_point', 'polarplot', 'pole', 'poly2symb', 'polyEval', 'polygon', 'polygone_rempli', 'polygonplot', 'polygonscatterplot', 'polyhedron', 'polynom', 'polynomial_regression', 'polynomial_regression_plot', 'position', 'poslbdLMQ', 'posubLMQ', 'potential', 'pow2exp', 'power_regression', 'power_regression_plot', 'powermod', 'powerpc', 'powexpand', 'powmod', 'prepend', 'preval', 'prevperm', 'prevprime', 'primpart', 'printf', 'prism', 'prism_graph', 'product', 'projection', 'proot', 'propFrac', 'propfrac', 'psrgcd', 'ptayl', 'purge', 'pwd', 'pyramid', 'python_compat', 'q2a', 'qr', 'quadric', 'quadrilateral', 'quantile', 'quartile1', 'quartile3', 'quartiles', 'quest', 'quo', 'quorem', 'quote', 'r2e', 'radical_axis', 'radius', 'ramene', 'rand', 'randMat', 'randNorm', 'randPoly', 'randbetad', 'randbinomial', 'randchisquare', 'randexp', 'randfisher', 'randgammad', 'randgeometric', 'randint', 'randmarkov', 'randmatrix', 'randmultinomial', 'randnorm', 'random', 'random_bipartite_graph', 'random_digraph', 'random_graph', 'random_network', 'random_planar_graph', 'random_regular_graph', 'random_sequence_graph', 'random_tournament', 'random_tree', 'random_variable', 'randperm', 'randpoisson', 'randpoly', 'randseed', 'randstudent', 'randvar', 'randvector', 'randweibulld', 'rank', 'ranm', 'ranv', 'rassembler_trigo', 'rat_jordan', 'rational', 'rationalroot', 'ratnormal', 'rcl', 'rdiv', 're', 'read', 'readrgb', 'readwav', 'real', 'realroot', 'reciprocation', 'rectangle', 'rectangle_droit', 'rectangle_gauche', 'rectangle_plein', 'rectangular_coordinates', 'recule', 'red', 'reduced_conic', 'reduced_quadric', 'ref', 'reflection', 'regroup', 'relabel_vertices', 'reliability_polynomial', 'rem', 'remain', 'remove', 'reorder', 'resample', 'residue', 'resoudre', 'resoudre_dans_C', 'resoudre_systeme_lineaire', 'resultant', 'reverse', 'reverse_graph', 'reverse_rsolve', 'revert', 'revlex', 'revlist', 'rgb', 'rhombus', 'rhombus_point', 'rhs', 'riemann_window', 'right', 'right_rectangle', 'right_triangle', 'risch', 'rm_a_z', 'rm_all_vars', 'rmbreakpoint', 'rmmod', 'rmwatch', 'romberg', 'rombergm', 'rombergt', 'rond', 'root', 'rootof', 'roots', 'rotate', 'rotation', 'round', 'row', 'rowAdd', 'rowDim', 'rowNorm', 'rowSwap', 'rowdim', 'rownorm', 'rowspace', 'rowswap', 'rref', 'rsolve', 'same', 'sample', 'samplerate', 'sans_factoriser', 'saute', 'scalarProduct', 'scalar_product', 'scatterplot', 'schur', 'sec', 'secant_solver', 'segment', 'seidel_spectrum', 'seidel_switch', 'select', 'semi_augment', 'seq', 'seqplot', 'seqsolve', 'sequence_graph', 'series', 'set_edge_attribute', 'set_edge_weight', 'set_graph_attribute', 'set_pixel', 'set_vertex_attribute', 'set_vertex_positions', 'shift', 'shift_phase', 'shortest_path', 'show_pixels', 'shuffle', 'sierpinski_graph', 'sign', 'signature', 'signe', 'similarity', 'simp2', 'simplex_reduce', 'simplifier', 'simplify', 'simpson', 'simult', 'sin', 'sin2costan', 'sincos', 'single_inter', 'sinh', 'sizes', 'slope', 'slopeat', 'slopeatraw', 'smith', 'smod', 'snedecor', 'snedecor_cdf', 'snedecor_icdf', 'snedecord', 'snedecord_cdf', 'snedecord_icdf', 'solid_line', 'solve', 'somme', 'sommet', 'sort', 'sorta', 'sortd', 'sorted', 'soundsec', 'spanning_tree', 'sphere', 'spline', 'split', 'spring', 'sq', 'sqrfree', 'sqrt', 'square', 'square_point', 'srand', 'sst', 'sst_in', 'st_ordering', 'star_graph', 'star_point', 'start', 'stdDev', 'stddev', 'stddevp', 'steffenson_solver', 'stereo2mono', 'str', 'strongly_connected_components', 'student', 'student_cdf', 'student_icdf', 'studentd', 'studentt', 'sturm', 'sturmab', 'sturmseq', 'style', 'subMat', 'subdivide_edges', 'subgraph', 'subs', 'subsop', 'subst', 'substituer', 'subtype', 'sum', 'sum_riemann', 'suppress', 'surd', 'svd', 'swapcol', 'swaprow', 'switch_axes', 'sylvester', 'symb2poly', 'symbol', 'syst2mat', 'tCollect', 'tExpand', 'table', 'tablefunc', 'tableseq', 'tabvar', 'tail', 'tan', 'tan2cossin2', 'tan2sincos', 'tan2sincos2', 'tangent', 'tangente', 'tanh', 'taux_accroissement', 'taylor', 'tchebyshev1', 'tchebyshev2', 'tcoeff', 'tcollect', 'tdeg', 'tensor_product', 'tetrahedron', 'texpand', 'thickness', 'threshold', 'throw', 'title', 'titre', 'tlin', 'tonnetz', 'topologic_sort', 'topological_sort', 'torus_grid_graph', 'total_degree', 'tourne_droite', 'tourne_gauche', 'tpsolve', 'trace', 'trail', 'trail2edges', 'trames', 'tran', 'transitive_closure', 'translation', 'transpose', 'trapeze', 'trapezoid', 'traveling_salesman', 'tree', 'tree_height', 'triangle', 'triangle_paper', 'triangle_plein', 'triangle_point', 'triangle_window', 'trig2exp', 'trigcos', 'trigexpand', 'triginterp', 'trigsimplify', 'trigsin', 'trigtan', 'trn', 'true', 'trunc', 'truncate', 'truncate_graph', 'tsimplify', 'tuer', 'tukey_window', 'tutte_polynomial', 'two_edge_connected_components', 'ufactor', 'ugamma', 'unapply', 'unarchive', 'underlying_graph', 'unfactored', 'uniform', 'uniform_cdf', 'uniform_icdf', 'uniformd', 'uniformd_cdf', 'uniformd_icdf', 'unitV', 'unquote', 'upper', 'user_operator', 'usimplify', 'valuation', 'vandermonde', 'variables_are_files', 'variance', 'version', 'vertex_connectivity', 'vertex_degree', 'vertex_distance', 'vertex_in_degree', 'vertex_out_degree', 'vertices', 'vertices_abc', 'vertices_abca', 'vpotential', 'web_graph', 'weibull', 'weibull_cdf', 'weibull_icdf', 'weibulld', 'weibulld_cdf', 'weibulld_icdf', 'weibullvariate', 'weight_matrix', 'weighted', 'weights', 'welch_window', 'wheel_graph', 'widget_size', 'wilcoxonp', 'wilcoxons', 'wilcoxont', 'with_sqrt', 'writergb', 'writewav', 'xcas_mode', 'xyztrange', 'zeros', 'ztrans']
#

missing=set(mostkeywordorig).difference(mostkeywords)
print("Missing",missing)
newkeywords=(set(mostkeywords).difference(mostkeywordorig)).difference(toremove+blacklist)
print("\nNew Keywords found:", newkeywords)

#undocumented keywords
#undocumented=['posubLMQ','poslbdLMQ','VAS_positive','VAS']
undocumented=[]

mostkeywords=mostkeywords+undocumented

mostkeywords=set(mostkeywords).difference(toremove)
mostkeywords=set(mostkeywords).difference(blacklist)
mostkeywords=set(mostkeywords).difference(moremethods)
mostkeywords=list(mostkeywords)
mostkeywords.sort()


# building auto-methods.pxi
Mi=open("auto-methods.pxi","w")
Mi.write("# file auto generated by mkkeywords.py\n")
s='cdef class GiacMethods_base:\n     """\n     Wrapper for a giac ``gen`` containing auto-generated methods.\n'
s+='\n     This class does not manage the ``gen`` inside in any way. It is just\n     a dumb wrapper.'
s+='\n     You almost certainly want to use one of the derived class\n     :class:`Pygen`  instead.\n     """\n\n'
Mi.write(s)

for i in mostkeywords+moremethods:
    p = Popen(["cas_help", i], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    doc = p.communicate()[0]

    doc = doc.replace("\n", "\n        ")  # Indent doc
    s =  "     def "+i+"(self,*args):\n"
    s += "        r'''From Giac's documentation:\n        "+doc+"\n        '''\n"
    s += "        return GiacMethods['"+i+"'](self,*args)\n\n"
    Mi.write(s)

Mi.close()

# building keywords.pxi
with open("keywords.pxi", "w") as Fi:
    Fi.write("# file auto generated by mkkeywords.py\n")
    Fi.write("blacklist = " + str(blacklist) + "\n\n")
    Fi.write("toremove = " + str(toremove) + "\n\n")
    Fi.write("moremethods = " + str(moremethods) + "\n\n")
    Fi.write("mostkeywords = " + str(mostkeywords) + "\n\n")

with open("newkeyword.pxi", "w") as Fi:
    Fi.write(str(list(set(mostkeywords).difference(mostkeywordorig))))
