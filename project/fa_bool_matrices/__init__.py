import sys

from project.fa_bool_matrices.fa_bool_matrices import *
from project.fa_bool_matrices.fa_boolean_matrices_dok import *

if sys.platform.startswith("linux"):
    from project.fa_bool_matrices.fa_boolean_matrices_cb import *
