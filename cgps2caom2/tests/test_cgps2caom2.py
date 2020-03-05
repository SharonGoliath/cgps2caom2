from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from astropy.io import fits

from cgps2caom2 import to_caom2, draw_cgps_blueprint
from caom2 import ObservationReader
from caom2pipe import manage_composable as mc

import os
import pytest
import sys


TEST_URI = 'ad:CGPS/CGPS_MC2_1420_MHz_I_image.fits'
TEST_URI_FHWM = 'ad:CGPS/CGPS_MD1_100_um_fwhm.txt'

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TESTDATA_DIR = os.path.join(THIS_DIR, 'data')


def test_draw():
    hdr1 = fits.Header()
    hdr1['INSTRUME'] = 'TEST'
    hdr1['OBSFREQ'] = '1420406000.0'
    test_blueprint = draw_cgps_blueprint(TEST_URI, [hdr1], local=False,
                                         cert=None)
    assert test_blueprint is not None
    assert test_blueprint._plan['Observation.telescope.name'] == 'DRAO-ST'
    assert test_blueprint._plan['Chunk.energy.specsys'] == 'TOPOCENT'
    assert test_blueprint._plan['Chunk.position.axis.axis1.cunit'] == 'deg'
    assert test_blueprint._plan['Chunk.polarization.axis.function.delta'] == \
        '1'
    assert test_blueprint._plan['Chunk.energy.restfrq'] == (['OBSFREQ'], None)
    assert test_blueprint._plan['Observation.intent'] == 'science'
    assert test_blueprint._plan['Plane.provenance.lastExecuted'] == (
        ['DATE-FTS'], None)


@pytest.mark.parametrize('test_name', ['MC2_DRAO-ST', 'MC2_FCRAO', 'MD1_IRAS'])
def test_main_app(test_name):
    location = os.path.join(TESTDATA_DIR, test_name)
    actual_file_name = os.path.join(
        location, '{}.actual.xml'.format(test_name))
    files = ' '.join(
        [os.path.join(location, name) for name in os.listdir(location) if
         name.endswith('header')])
    uris = ' '.join(
        ['ad:CGPS/{}'.format(name.split('.header')[0]) for name in
         os.listdir(location) if name.endswith('header')])
    sys.argv = \
        (f'cgps2caom2 --local {files} --observation CGPS {test_name} -o '
         f'{actual_file_name} {uris}').split()
    to_caom2()

    test_result = mc.compare_observations(
        actual_file_name, os.path.join(location, f'{test_name}.xml'))
    if test_result is not None:
        raise AssertionError(test_result)


def _read_obs(fname):
    assert os.path.exists(fname)
    reader = ObservationReader(False)
    result = reader.read(fname)
    return result
