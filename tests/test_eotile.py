# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

import geopandas as gp
from shapely import wkt

from eotile.eotile.create_tile_shp_from_AOI import *
from eotile.eotiles.eotiles import create_tiles_list_L8, create_tiles_list_S2


class TestEOTile(unittest.TestCase):
    def test_create_tiles_file_from_AOI(self):
        output_path = "data/output"
        create_tiles_file_from_AOI(
            aoi_filepath="data/test_data/illinois.shp",
            aux_data_dirpath="data/aux_data",
            out_dirpath=output_path,
            s2=True,
            l8=False,
        )
        l8file = gp.read_file(output_path + "/illinois_tiles_L8.shp")
        self.assertEqual(l8file.count().geometry, 18)
        polygon_test = wkt.loads(
            "POLYGON ((-92.76509068409111 41.16654042276556, -92.7655 41.1666, -92.75222227023833"
            " 41.20908647471725, -92.74229393529802 41.24085545623727, -92.31883652795568"
            " 42.59584706653722, -92.30820221301863 42.6298750638544, -92.29559999999999 42.6702,"
            " -92.29516926900379 42.67013726441029, -90.0903 42.349, -90.10354172180196"
            " 42.31079408343177, -90.59568479060121 40.89082942117895, -90.60890000000001 "
            "40.8527, -92.76509068409111 41.16654042276556))"
        )
        self.assertTrue(polygon_test in l8file["geometry"])

        s2file = gp.read_file(output_path + "/illinois_tiles_S2.shp")
        self.assertEqual(s2file.count().geometry, 33)
        polygon_test = wkt.loads(
            "POLYGON ((-91.766187862 43.346200009, -90.533217951 43.326246335,"
            " -90.56881764800001 42.426541772, -91.784009944 42.445880705, "
            "-91.766187862 43.346200009))"
        )
        self.assertTrue(polygon_test in s2file["geometry"])

    def test_tile_list_utils_s2(self):
        ls2 = create_tiles_list_S2(
            "data/aux_data/S2A_OPER_GIP_TILPAR_MPC__20140923T000000_V20000101T000000_20200101T000000_B00.xml",
            "data/test_data/illinois.shp",
        )
        self.assertEqual(
            [
                "43.346200009",
                "-91.766187862",
                "43.326246335",
                "-90.533217951",
                "42.426541772",
                "-90.568817648",
                "42.445880705",
                "-91.784009944",
            ],
            ls2[0].BB,
        )
        self.assertEqual(len(ls2), 33)
        self.assertTrue(
            get_tile(ls2, ls2[1].ID).BB
            in [
                [
                    "43.346200009",
                    "-91.766187862",
                    "43.326246335",
                    "-90.533217951",
                    "42.426541772",
                    "-90.568817648",
                    "42.445880705",
                    "-91.784009944",
                ],
                [
                    "43.326246335",
                    "-90.533217951",
                    "43.293031723",
                    "-89.301928866",
                    "42.394349602",
                    "-89.355217574",
                    "42.426541772",
                    "-90.568817648",
                ],
                [
                    "42.426541772",
                    "-90.568817648",
                    "42.394349602",
                    "-89.355217574",
                    "41.495474123",
                    "-89.406124539",
                    "41.526672311",
                    "-90.602824028",
                ],
                [
                    "41.54541366",
                    "-91.801033713",
                    "41.526672311",
                    "-90.602824028",
                    "40.626639727",
                    "-90.635319213",
                    "40.64479965",
                    "-91.817300377",
                ],
                [
                    "41.526672311",
                    "-90.602824028",
                    "41.495474123",
                    "-89.406124539",
                    "40.596408719",
                    "-89.454772217",
                    "40.626639727",
                    "-90.635319213",
                ],
                [
                    "40.64479965",
                    "-91.817300377",
                    "40.626639727",
                    "-90.635319213",
                    "39.726445843",
                    "-90.666379316",
                    "39.744039563",
                    "-91.832848125",
                ],
                [
                    "40.626639727",
                    "-90.635319213",
                    "40.596408719",
                    "-89.454772217",
                    "39.697156754",
                    "-89.501274127",
                    "39.726445843",
                    "-90.666379316",
                ],
                [
                    "39.744039563",
                    "-91.832848125",
                    "39.726445843",
                    "-90.666379316",
                    "38.826092537",
                    "-90.696074964",
                    "38.84313441",
                    "-91.847712385",
                ],
                [
                    "39.726445843",
                    "-90.666379316",
                    "39.697156754",
                    "-89.501274127",
                    "38.797721547",
                    "-89.545735626",
                    "38.826092537",
                    "-90.696074964",
                ],
                [
                    "38.826092537",
                    "-90.696074964",
                    "38.797721547",
                    "-89.545735626",
                    "37.898106377",
                    "-89.5882546",
                    "37.92558175",
                    "-90.724471764",
                ],
                [
                    "37.92558175",
                    "-90.724471764",
                    "37.898106377",
                    "-89.5882546",
                    "36.998314508",
                    "-89.628922085",
                    "37.024915488",
                    "-90.75163072",
                ],
                [
                    "43.326246335",
                    "-89.466782049",
                    "43.346200009",
                    "-88.233812138",
                    "42.445880705",
                    "-88.215990056",
                    "42.426541772",
                    "-89.431182352",
                ],
                [
                    "43.346200009",
                    "-88.233812138",
                    "43.352855392",
                    "-87",
                    "42.452330961",
                    "-87",
                    "42.445880705",
                    "-88.215990056",
                ],
                [
                    "42.394349602",
                    "-90.644782426",
                    "42.426541772",
                    "-89.431182352",
                    "41.526672311",
                    "-89.397175972",
                    "41.495474123",
                    "-90.593875461",
                ],
                [
                    "42.426541772",
                    "-89.431182352",
                    "42.445880705",
                    "-88.215990056",
                    "41.54541366",
                    "-88.198966287",
                    "41.526672311",
                    "-89.397175972",
                ],
                [
                    "42.445880705",
                    "-88.215990056",
                    "42.452330961",
                    "-87",
                    "41.551664522",
                    "-87",
                    "41.54541366",
                    "-88.198966287",
                ],
                [
                    "41.495474123",
                    "-90.593875461",
                    "41.526672311",
                    "-89.397175972",
                    "40.626639727",
                    "-89.364680787",
                    "40.596408719",
                    "-90.545227783",
                ],
                [
                    "41.526672311",
                    "-89.397175972",
                    "41.54541366",
                    "-88.198966287",
                    "40.64479965",
                    "-88.182699623",
                    "40.626639727",
                    "-89.364680787",
                ],
                [
                    "41.54541366",
                    "-88.198966287",
                    "41.551664522",
                    "-87",
                    "40.650856516",
                    "-87",
                    "40.64479965",
                    "-88.182699623",
                ],
                [
                    "40.596408719",
                    "-90.545227783",
                    "40.626639727",
                    "-89.364680787",
                    "39.726445843",
                    "-89.333620684",
                    "39.697156754",
                    "-90.498725873",
                ],
                [
                    "40.626639727",
                    "-89.364680787",
                    "40.64479965",
                    "-88.182699623",
                    "39.744039563",
                    "-88.167151875",
                    "39.726445843",
                    "-89.333620684",
                ],
                [
                    "40.64479965",
                    "-88.182699623",
                    "40.650856516",
                    "-87",
                    "39.749907519",
                    "-87",
                    "39.744039563",
                    "-88.167151875",
                ],
                [
                    "39.697156754",
                    "-90.498725873",
                    "39.726445843",
                    "-89.333620684",
                    "38.826092537",
                    "-89.303925036",
                    "38.797721547",
                    "-90.454264374",
                ],
                [
                    "39.726445843",
                    "-89.333620684",
                    "39.744039563",
                    "-88.167151875",
                    "38.84313441",
                    "-88.152287615",
                    "38.826092537",
                    "-89.303925036",
                ],
                [
                    "39.744039563",
                    "-88.167151875",
                    "39.749907519",
                    "-87",
                    "38.848818252",
                    "-87",
                    "38.84313441",
                    "-88.152287615",
                ],
                [
                    "38.797721547",
                    "-90.454264374",
                    "38.826092537",
                    "-89.303925036",
                    "37.92558175",
                    "-89.275528236",
                    "37.898106377",
                    "-90.4117454",
                ],
                [
                    "38.826092537",
                    "-89.303925036",
                    "38.84313441",
                    "-88.152287615",
                    "37.94208532",
                    "-88.138073932",
                    "37.92558175",
                    "-89.275528236",
                ],
                [
                    "38.84313441",
                    "-88.152287615",
                    "38.848818252",
                    "-87",
                    "37.947589572",
                    "-87",
                    "37.94208532",
                    "-88.138073932",
                ],
                [
                    "37.898106377",
                    "-90.4117454",
                    "37.92558175",
                    "-89.275528236",
                    "37.024915488",
                    "-89.24836928",
                    "36.998314508",
                    "-90.371077915",
                ],
                [
                    "37.92558175",
                    "-89.275528236",
                    "37.94208532",
                    "-88.138073932",
                    "37.040893543",
                    "-88.12448023",
                    "37.024915488",
                    "-89.24836928",
                ],
                [
                    "37.94208532",
                    "-88.138073932",
                    "37.947589572",
                    "-87",
                    "37.046222476",
                    "-87",
                    "37.040893543",
                    "-88.12448023",
                ],
                [
                    "36.998314508",
                    "-90.371077915",
                    "37.024915488",
                    "-89.24836928",
                    "36.124095832",
                    "-89.222391385",
                    "36.098349195",
                    "-90.332177171",
                ],
                [
                    "37.024915488",
                    "-89.24836928",
                    "37.040893543",
                    "-88.12448023",
                    "36.13956045",
                    "-88.111478032",
                    "36.124095832",
                    "-89.222391385",
                ],
            ]
        )

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

    def test_tile_list_utils_l8(self):
        l8 = create_tiles_list_L8(
            "data/aux_data/wrs2_descending/", "data/test_data/illinois.shp"
        )
        self.assertEqual(len(l8), 18)
        self.assertTrue(
            l8[1].ID
            in [
                25030,
                25031,
                25032,
                25033,
                23030,
                23031,
                23032,
                23033,
                23034,
                24030,
                24031,
                24032,
                24033,
                24034,
                22031,
                22032,
                22033,
                22034,
            ]
        )

    def test_read_write_tiles_bb(self):
        ll8 = create_tiles_list_L8(
            "data/aux_data/wrs2_descending/", "data/test_data/illinois.shp"
        )
        test_file_path = "data/output/test_read_write.shp"
        write_tiles_bb(ll8, test_file_path)

        read_file = read_tile_list_from_file(
            "/home/mathis/Documents/EODAG/EOTILE/eotile/data/test_data2/illinois2.shp"
        )
        ID_list = []
        for elt in read_file:
            ID_list.append(elt.ID)
        self.assertTrue("25030" in ID_list)


if __name__ == "__main__":
    logging.basicConfig(filename="test_eotile.log", level=logging.INFO)
    unittest.main()
