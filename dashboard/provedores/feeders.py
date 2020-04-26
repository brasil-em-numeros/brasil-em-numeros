from . import ibge
from . import pdt
from collections import OrderedDict


def implemented_feeders():

    d = OrderedDict()
    for dkt in (pdt.id, ibge.id):
        d[dkt['name']] = dkt
        d.move_to_end(dkt['name'])

    return d
