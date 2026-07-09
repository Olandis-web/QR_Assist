# This __init__.py bridges the lowercase 'database' package to the actual 'Database' package
# to handle case-sensitivity on Linux.
#
# We import conexion first to avoid circular imports,
# since Database/*.py modules do 'from database import conexion'.

# Import the conexion module (not the function) so "conexion.conexion()" works
from Database import conexion as _conexion_module

# Expose the actual modules so "from database import X" finds them
import sys

# Assign conexion as the module so code like "conexion.conexion()" works
globals()['conexion'] = _conexion_module

# Now import the actual modules from the Database directory
# (must be after conexion assignment to avoid circular imports)
from Database import usuarios as _usuarios_module
from Database import empleados as _empleados_module
from Database import reportes as _reportes_module

# Create module references so "from database import X" finds them
for _name, _mod in [("usuarios", _usuarios_module), 
                     ("empleados", _empleados_module), 
                     ("reportes", _reportes_module)]:
    # Create a module-like object in sys.modules so imports find it
    if _name not in sys.modules:
        sys.modules[f"database.{_name}"] = _mod
    globals()[_name] = _mod

# Re-export all public names from each module for convenience
def _re_export(module):
    for name in dir(module):
        if not name.startswith('_'):
            globals()[name] = getattr(module, name)

_re_export(_usuarios_module)
_re_export(_empleados_module)
_re_export(_reportes_module)