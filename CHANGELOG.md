# Changelog

## 1.7.1 - 2020/05/29

### Changed

	- Fixed a bug with singular matrices when the last layers is identical to the
	transmission medium

### Removed

	- The whole media/ package

## 1.7.0 - 2020/05/20

### Changed

	- Media management now has its own package : mediapack

### Removed

	- HDF5 capabilities (unused)

## 1.6.0 - 2020/03/20

### Changed

	- Possibility to instaciate media through arguments to __init__()
	- New tests

### Fixed

	- Loading of fluid media

## 1.5.2 - 2019/06/24

### Changed

  - The testsuite now uses pytest instead of unittest
	- Parts of the code using numpy.matrix have been rewritten to use numpy.ndarray

## 1.5.2 - 2019/06/24

### Changed

  - Change the backing condition used in `compute_fields`

## 1.5.1 - 2019/06/07

### Fixed

  - Fix pyYAML warning with `safe_load` instead of `load`

## 1.5 - 2019/06/04

### Changed

  - Code cleanup
  - Many changes over the last minors, a major seemed needed

## 1.4.10 - 2019/06/03

### Changed

  - The handling of rigid backing condition has been improved for PEM (the
	previous one would give inaccurate results in some cases)

### Fixed

  - Github-reported security issues in requirements.txt
  - Bumped PyYAML version in setup for security reasons (CVE-2017-18342)

## 1.4.9 - 2019/02/26

### Fixed

  - Minor bugs and typos in tests and code

## 1.4.8 - 2019/02/26

### Changed

  - Some of the parameters set as mandatory for EqF are now optional... as in the
		underlying theory

### Added

  - a DrawsManager class as been added to help with stochastic layers


## 1.4.7 - 2018/12/17

### Changed

  - call to `Solver.solve()` leading to a single resultset will return directly this
		resultset and not a 1-element list containing it

### Added

  - the function `Solver.compute_fields()` allows to compute the fields at any interface of
		the multilayer
  - tests and some documentation
  - CI

## 1.4.6 - 2018/08/20

### Fixed

  - Dependencies issues

## 1.4.5 - 2018/05/17

### Added

  - use the isothermal limit for the dynamic compressibility in the screen model (cf, JASA-EL review)

## 1.4.4 - 2018/01/25

### Added

  - Simplified model for thin screen/films/veils

## 1.4.3 - 2017/10/23

### Added

  - acoustic indicators computation

## 1.4.2 - 2017/10/12

### Added

  - save all intermediate wavenumbers in PEM material

## 1.4.1 - 2017/10/12

### Added

  - weak requirements on the medium classes mandatory parameters when reading yaml files with force

## 1.4.0 - 2017/10/11

### Added

  - Add a lot of tests to the testbase
  - Add possibility to force the way from_yaml imports a material
  - Add possibility of adding pre update_frequency hooks

### Fixed

  - error in back propagation matrices
  - bug in the equivalent fluid implementation

## 1.3.3 - 2017/10/06

### Fixed

  - HDF5 export issue when only 1 analysis

## 1.3.2 - 2017/10/05

### Added

  - double layers test cases to check for back propagation through transparent interfaces

### Fixed

  - error in the back-propagation sequence

## 1.3.1 - 2017/10/05

### Added

  - All metadata in HDF5 exports

## 1.3.0 - 2017/10/05

### Added

  - HDF5 exporter
  - 'loaders' submodule becomes 'utils'

### Fixed

  - creation of the result structure w/ transmission coefficients

## 1.2.2 - 2017/10/03

### Fixed

  - issues with the resultset & returned structure for stochastic analysis

## 1.2.1 - 2017/10/02

### Added

  - Updated test cases
  - Updated examples
  - Reduced result structure when only 1 analysis

### Fixed

  - cleaner code

## 1.2.0 - 2017-09-29

### Added

  - stochastic analyses w/ automatic range generation

### Fixed

  - bug in shear modulus formula

## 1.1.0 - 2017/09/27

First released version.
