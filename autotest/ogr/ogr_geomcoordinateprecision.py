#!/usr/bin/env pytest
# -*- coding: utf-8 -*-
###############################################################################
# Project:  GDAL/OGR Test Suite
# Purpose:  Test ogr.GeomCoordinatePrecision
# Author:   Even Rouault <even dot rouault at spatialys.com>
#
###############################################################################
# Copyright (c) 2024, Even Rouault <even dot rouault at spatialys.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import pytest

from osgeo import ogr, osr


def test_ogr_geomcoordinate_precision():

    prec = ogr.CreateGeomCoordinatePrecision()
    assert prec.GetXYResolution() == 0
    assert prec.GetZResolution() == 0
    assert prec.GetMResolution() == 0

    prec.Set(1e-9, 1e-3, 1e-2)
    assert prec.GetXYResolution() == 1e-9
    assert prec.GetZResolution() == 1e-3
    assert prec.GetMResolution() == 1e-2

    with pytest.raises(Exception, match="Received a NULL pointer"):
        prec.SetFromMetre(None, 0, 0, 0)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    prec.SetFromMetre(srs, 1e-3, 1e-3, 1e-1)
    assert prec.GetXYResolution() == pytest.approx(8.983152841195213e-09)
    assert prec.GetZResolution() == 1e-3
    assert prec.GetMResolution() == 1e-1

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4979)
    prec.SetFromMetre(srs, 1e-3, 1e-3, 1e-1)
    assert prec.GetXYResolution() == pytest.approx(8.983152841195213e-09)
    assert prec.GetZResolution() == 1e-3
    assert prec.GetMResolution() == 1e-1

    srs = osr.SpatialReference()
    srs.SetFromUserInput("EPSG:4269+8228")  # "NAD83 + NAVD88 height (ft)"
    prec.SetFromMetre(srs, 1e-3, 1e-3, 1e-1)
    assert prec.GetXYResolution() == pytest.approx(8.983152841195213e-09)
    assert prec.GetZResolution() == pytest.approx(0.0032808398950131233)
    assert prec.GetMResolution() == 1e-1

    assert prec.GetFormats() is None
    assert prec.GetFormatSpecificOptions("foo") == {}
    with pytest.raises(Exception, match="Received a NULL pointer"):
        prec.GetFormatSpecificOptions(None)
    prec.SetFormatSpecificOptions("my_format", {"key": "value"})
    assert prec.GetFormats() == ["my_format"]
    assert prec.GetFormatSpecificOptions("my_format") == {"key": "value"}
