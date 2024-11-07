#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Generate test_s104.h5
# Author:   Even Rouault <even dot rouault at spatialys.com>
#
###############################################################################
# Copyright (c) 2023, Even Rouault <even dot rouault at spatialys.com>
#
# SPDX-License-Identifier: MIT
###############################################################################

import os

import h5py
import numpy as np


def generate(filename, version):
    f = h5py.File(os.path.join(os.path.dirname(__file__), f"{filename}.h5"), "w")
    WaterLevel = f.create_group("WaterLevel")
    WaterLevel_01 = WaterLevel.create_group("WaterLevel.01")
    Group_001 = WaterLevel_01.create_group("Group_001")

    WaterLevel.attrs["dataCodingFormat"] = np.uint8(2)
    WaterLevel.attrs["minDatasetHeight"] = np.float32(1)
    WaterLevel.attrs["maxDatasetHeight"] = np.float32(2)

    values_struct_type = np.dtype(
        [
            ("waterLevelHeight", "f4"),
            ("waterLevelTrend", "u1"),
        ]
    )
    values = Group_001.create_dataset("values", (2, 3), dtype=values_struct_type)
    data = np.array(
        [(-123, 0), (1, 1), (2, 2), (3, 3), (4, 2), (5, 1)],
        dtype=values_struct_type,
    ).reshape(values.shape)
    values[...] = data

    Group_001.attrs["timePoint"] = "20190606T120000Z"

    WaterLevel_01.attrs["gridOriginLongitude"] = np.float64(2)
    WaterLevel_01.attrs["gridOriginLatitude"] = np.float64(48)
    WaterLevel_01.attrs["gridSpacingLongitudinal"] = np.float64(0.4)
    WaterLevel_01.attrs["gridSpacingLatitudinal"] = np.float64(0.5)
    WaterLevel_01.attrs["numPointsLongitudinal"] = np.uint32(values.shape[1])
    WaterLevel_01.attrs["numPointsLatitudinal"] = np.uint32(values.shape[0])

    WaterLevel_01.attrs["numberOfTimes"] = np.uint32(1)
    WaterLevel_01.attrs["timeRecordInterval"] = np.uint16(3600)
    WaterLevel_01.attrs["dateTimeOfFirstRecord"] = "20190606T120000Z"
    WaterLevel_01.attrs["dateTimeOfLastRecord"] = "20190606T120000Z"

    WaterLevel_01.attrs["numGRP"] = np.uint32(1)
    WaterLevel_01.attrs["startSequence"] = "0,0"

    Group_F = f.create_group("Group_F")
    Group_F_WaterLevel_struct_type = np.dtype(
        [
            ("code", "S20"),
            ("name", "S20"),
            ("uom.name", "S20"),
            ("fillValue", "S20"),
            ("datatype", "S20"),
            ("lower", "S20"),
            ("upper", "S20"),
            ("closure", "S20"),
        ]
    )
    Group_F_WaterLevel = Group_F.create_dataset(
        "WaterLevel", (3,), dtype=Group_F_WaterLevel_struct_type
    )
    Group_F_WaterLevel[...] = np.array(
        [
            (
                "waterLevelHeight",
                "Water Level Height",
                "metres",
                "-123.0",
                "H5T_FLOAT",
                "-99.99",
                "99.99",
                "closedInterval",
            ),
            ("waterLevelTrend", "Water Level Trend", "", "0", "H5T_ENUM", "", "", ""),
            (
                "waterLevelTime",
                "Water Level Time",
                "DateTime",
                "",
                "H5T_STRING",
                "19000101T000000Z",
                "21500101T000000Z9",
                "closedInterval",
            ),
        ],
        dtype=Group_F_WaterLevel_struct_type,
    )

    f.attrs["issueDate"] = "2023-12-31"
    f.attrs["geographicIdentifier"] = "Somewhere"
    f.attrs["verticalDatum"] = np.int16(12)
    f.attrs["horizontalCRS"] = np.int32(4326)
    f.attrs["verticalCS"] = np.int32(6498)  # Depth, metres, orientation down
    f.attrs["verticalCoordinateBase"] = np.int32(2)
    f.attrs["verticalDatumReference"] = np.int32(1)
    f.attrs["productSpecification"] = version
    f.attrs[
        "producer"
    ] = "Generated by autotest/gdrivers/data/s104/generate_test.py (not strictly fully S104 compliant)"
    f.attrs["metadata"] = f"MD_{filename}.xml"

    open(os.path.join(os.path.dirname(__file__), f.attrs["metadata"]), "wb").write(
        b"<nothing/>"
    )


generate("test_s104_v1.1", "INT.IHO.S-104.1.1")
