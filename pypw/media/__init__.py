import os
import yaml

from .medium import Medium
from .air import Air
from .eqf import EqFluidJCA
from .elastic import Elastic
#from .fluid import Fluid


# TODO: refactor to use Medium.MEDIUMTYPE
__MEDIUMCLASSES_MAP = {
    'eqf_jca': EqFluidJCA,
    'elastic': Elastic,
#    'fluid': Fluid
}


def from_yaml(filename):
    """Reads medium definition from YAML file filename. Raises an IOError if the file
    is not found, ValueError if medium type is not known and a LookupError if the
    parameter definition is incomplete."""

    if not os.path.exists(filename):
        raise IOError(f'Unable to locate file {filename}')

    with open(filename) as fh:
        yaml_data = yaml.load(fh)

    if yaml_data.get('medium_type') is None:
        raise LookupError('Unspecified medium type')

    medium_class = __MEDIUMCLASSES_MAP.get(yaml_data['medium_type'])
    if medium_class is None:
        raise ValueError(f'Medium type is not known')
    else:
        medium = medium_class()
        medium.from_dict(yaml_data)
        return medium
