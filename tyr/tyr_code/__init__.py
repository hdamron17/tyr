import os
import os.path

_PKG_ROOT = os.path.dirname(__file__)

_header_list = [f for f in os.listdir(_PKG_ROOT) if f.endswith(".tyr")]

def _load_header(name):
  def _load_file(f=name):
    return open(os.path.join(_PKG_ROOT, name)).read()
  return _load_file

for _name in _header_list:
  globals()[_name.rsplit('.')[0]] = _load_header(_name)
