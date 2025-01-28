#!/usr/bin/env pytest
# -*- coding: utf-8 -*-
###############################################################################
#
# Project:  GDAL/OGR Test Suite
# Purpose:  gdal2tiles.py testing
# Author:   Gregory Bataille <gregory.bataille@gmail.com>
#
###############################################################################
# Copyright (c) 2017, Gregory Bataille <gregory.bataille@gmail.com>
#
# SPDX-License-Identifier: MIT
###############################################################################

from unittest import TestCase, mock

from osgeo_utils import gdal2tiles


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class UpdateAlphaValueForNonAlphaInputsTest(TestCase):
    def setUp(self):
        self.DEFAULT_OPTIONS = {
            "srcnodata": None,
            "verbose": True,
        }
        self.DEFAULT_ATTRDICT_OPTIONS = AttrDict(self.DEFAULT_OPTIONS)

        self.RASTER_COUNT = 4

        self.mock_dataset = mock.MagicMock()
        self.mock_dataset.RasterCount = self.RASTER_COUNT

    def test_do_nothing_on_2_or_4_bands_inputs(self):
        self.mock_dataset.RasterCount = 4
        modif_dataset = gdal2tiles.update_alpha_value_for_non_alpha_inputs(
            self.mock_dataset
        )
        self.assertEqual(modif_dataset, self.mock_dataset)
