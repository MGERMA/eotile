# -*- coding: utf-8 -*-
"""
:author: mgerma
:organization: CS-Group
:copyright: 2021 CS-Group France. All rights reserved.
:license: see LICENSE file.
"""

import logging
import unittest
from pathlib import Path

from eotile.eotile_module import build_nominatim_request, input_matcher
from eotile.eotile_module import main as eomain
from eotile.eotiles.eotiles import create_tiles_list_eo, get_tile, write_tiles_bb
from eotile.eotiles.get_bb_from_tile_id import get_tiles_from_tile_id, tile_id_matcher


class TestEOTile(unittest.TestCase):
    def test_tile_list_utils_s2(self):
        ls2 = create_tiles_list_eo(
            Path("eotile/data/aux_data/s2/s2_no_overlap_S2.shp"),
            Path("tests/test_data/illinois.shp"),
            "S2",
        )
        self.assertEqual(len(ls2), 33)

        self.assertTrue(
            ls2[1].ID
            in [
                "15TXH",
                "15TYH",
                "15TYG",
                "15TXF",
                "15TYF",
                "15TXE",
                "15TYE",
                "15SXD",
                "15SYD",
                "15SYC",
                "15SYB",
                "16TCN",
                "16TDN",
                "16TBM",
                "16TCM",
                "16TDM",
                "16TBL",
                "16TCL",
                "16TDL",
                "16TBK",
                "16TCK",
                "16TDK",
                "16SBJ",
                "16SCJ",
                "16SDJ",
                "16SBH",
                "16SCH",
                "16SDH",
                "16SBG",
                "16SCG",
                "16SDG",
                "16SBF",
                "16SCF",
            ]
        )

        self.assertTrue(get_tile(ls2, "15TXF") is not None)

    def test_tile_list_utils_l8(self):
        l8 = create_tiles_list_eo(
            Path("eotile/data/aux_data/wrs2_descending/"),
            Path("tests/test_data/illinois.shp"),
            "L8",
        )
        self.assertEqual(len(l8), 18)
        self.assertTrue(
            l8[1].ID
            in [
                "25030",
                "25031",
                "25032",
                "25033",
                "23030",
                "23031",
                "23032",
                "23033",
                "23034",
                "24030",
                "24031",
                "24032",
                "24033",
                "24034",
                "22031",
                "22032",
                "22033",
                "22034",
            ]
        )

    def test_read_write_tiles_bb(self):
        ll8 = create_tiles_list_eo(
            Path("eotile/data/aux_data/wrs2_descending/"),
            Path("tests/test_data/illinois.shp"),
            "L8",
        )
        write_tiles_bb(ll8, Path("/tmp/test_read_write.shp"))

        id_list = []
        for elt in ll8:
            id_list.append(elt.ID)
        self.assertTrue("25030" in id_list)

    def test_input_matcher(self):
        polygon = "POLYGON((1 1,5 1,5 5,1 5,1 1))"
        mpoly = "MULTIPOLYGON(((1 1,5 1,5 5,1 5,1 1),(2 2,2 3,3 3,3 2,2 2)),((6 3,9 2,9 4,6 3)))"

        bbox1 = "['36.9701313', '42.5082935', '-91.5130518', '-87.0199244']"
        bbox2 = "'36.9701313', '42.5082935', '-91.5130518', '-87.0199244'"
        bbox3 = "'36.9701313','42.5082935','-91.5130518','-87.0199244'"

        location1 = "Toulouse"
        location2 = "Nowhere"
        location3 = "France"

        tile_id1 = "31TCJ"
        tile_id2 = "199030"

        file1 = "/tmp"
        file2 = "/dev/null"

        test_list = [
            polygon,
            mpoly,
            bbox1,
            bbox2,
            bbox3,
            location1,
            location3,
            tile_id1,
            tile_id2,
            file1,
            file2,
        ]

        with self.assertRaises(ValueError):
            input_matcher(location2)

        out_list = []
        for elt in test_list:
            out_list.append(input_matcher(elt))

        self.assertListEqual(
            out_list,
            [
                "wkt",
                "wkt",
                "bbox",
                "bbox",
                "bbox",
                "location",
                "location",
                "tile_id",
                "tile_id",
                "file",
                "file",
            ],
        )

    def test_id_matcher(self):
        test_id_srtm = "N02W102"
        test_id_cop = "S02W102"
        test_id_s2 = "18SWJ"
        test_id_l8 = "12033"
        self.assertEqual(tile_id_matcher(test_id_l8), (False, True, False, False))
        self.assertEqual(tile_id_matcher(test_id_s2), (True, False, False, False))
        self.assertEqual(tile_id_matcher(test_id_cop), (False, False, True, True))
        self.assertEqual(tile_id_matcher(test_id_srtm), (False, False, True, True))

    def test_get_tiles_from_tile_id(self):
        output_s2, output_l8, output_srtm, output_cop = get_tiles_from_tile_id(
            "31TCJ", Path("eotile/data/aux_data"), False, False, srtm=True, cop=True
        )
        self.assertEqual(len(output_s2), 1)
        self.assertEqual(len(output_l8), 4)
        self.assertEqual(len(output_srtm), 4)
        self.assertEqual(len(output_cop), 4)

        output_s2, output_l8, output_srtm, output_cop = get_tiles_from_tile_id(
            "200035", Path("eotile/data/aux_data"), False, False, srtm=True, cop=True
        )
        self.assertEqual(len(output_s2), 8)
        self.assertEqual(len(output_l8), 1)

    def test_main_module(self):
        output_s2, output_l8, output_srtm, output_cop = eomain(
            "-74.657, 39.4284, -72.0429, 41.2409", s2_only=False, l8_only=False, srtm=True, cop=True
        )
        self.assertEqual(len(output_s2), 12)
        self.assertEqual(len(output_l8), 9)
        self.assertEqual(len(output_srtm), 7)
        self.assertEqual(len(output_cop), 9)

    def test_main_module_2(self):
        output_s2, output_l8, output_srtm, output_cop = eomain(
            "tests/test_data/illinois.shp", s2_only=False, l8_only=False, srtm=True, cop=True
        )
        self.assertEqual(len(output_s2), 33)
        self.assertEqual(len(output_l8), 18)
        self.assertEqual(len(output_srtm), 27)
        self.assertEqual(len(output_cop), 27)

    def test_main_module_3(self):
        output_s2, output_l8, output_srtm, output_cop = eomain(
            "Toulouse",
            s2_only=False,
            l8_only=False,
            srtm=True,
            cop=True,
            threshold=0.1,
            min_overlap=0.001,
        )
        self.assertEqual(len(output_s2), 1)
        self.assertEqual(len(output_l8), 2)
        self.assertEqual(len(output_srtm), 1)
        self.assertEqual(len(output_cop), 1)

    def test_build_nominatim_request(self):
        self.assertTrue(
            (build_nominatim_request(None, "Toulouse", "0.1").area - 0.013155945340939995) < 0.005
        )


if __name__ == "__main__":
    logging.basicConfig(filename="test_eotile.log", level=logging.INFO)
    unittest.main()
