import yaml

from .models import Locus
from .schemas import LocusSchema


def load_locus_yaml(fpath: str) -> Locus:
    schema = LocusSchema()
    with open(fpath) as handle:
        yd = yaml.load(handle)
    unmarshalled = schema.load(yd)
    if len(unmarshalled.errors) == 0:
        raise ValueError("Could not load Locus because {0}".format(unmarshalled.errors))
    return unmarshalled.data
