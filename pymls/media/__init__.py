import os
import yaml

from .air import Air
from .eqf import EqFluidJCA
from .elastic import Elastic
from .pem import PEM
from .fluid import Fluid


__MEDIUMCLASSES_MAP = {
    _.MEDIUM_TYPE: _ for _ in [EqFluidJCA, Elastic, PEM, Fluid]
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
