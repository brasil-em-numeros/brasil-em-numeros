from . import ibge
from . import pdt


def lista():

    return {
        d['name'] : d for d in [
            ibge.id, pdt.id
        ]
    }
