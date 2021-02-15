# -*- coding: utf-8 -*-
"""
Generate tile list according AOI

:author: jsiefert, msavinaud
:organization: CS-Group
:copyright: 2021 CS-Group France. All rights reserved.
:license: see LICENSE file.
"""

import argparse
import os
import sys

from eotile.utils.tile_list_utils import L8Tile, S2Tile


def get_bb_from_tile_id(tile_id, aux_data_dirpath, is_s2, is_l8):
    """Returns the bounding box of a tile designated by its ID.

    :param tile_id: The identifier of the tile
    :param aux_data_dirpath: Path to the input aux data
    :param is_s2: Is he requested tile a Sentinel 2 tile
    :type is_s2: Boolean
    :param is_l8: Is he requested tile a Landscape 8 tile
    :type is_l8: Boolean
    :return: A bounding box
    :rtype: #TODO: Precise this
    """

    # S2 tiles grig
    filename_tiles_S2 = os.path.join(
        aux_data_dirpath,
        "S2A_OPER_GIP_TILPAR_MPC__20140923T000000_V20000101T000000_20200101T000000_B00.xml",
    )

    # L8 tiles grid
    filename_tiles_L8 = os.path.join(
        aux_data_dirpath, "wrs2_descending", "wrs2_descending.shp"
    )

    if is_s2:
        tile = S2Tile.from_tile_id(tile_id, filename_tiles_S2)
    elif is_l8:
        tile = L8Tile.from_tile_id(tile_id, filename_tiles_L8)
    else:
        return None
    return tile.BB


def build_parser():
    """Creates a parser suitable for parsing a command line invoking this program.

    :return: An parser.
    :rtype: :class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("tile_id", help="tile_id")
    parser.add_argument("auxdata_dirpath", help="path to aux data directory")

    parser.add_argument(
        "-s2", action="store_true", help="output S2 tiles which intersect the aoi"
    )
    parser.add_argument(
        "-l8", action="store_true", help="output L8 tiles which intersect the aoi"
    )
    return parser


def main(arguments=None):
    """
    Command line interface to perform

    :param list arguments: list of arguments
    """

    arg_parser = build_parser()

    args = arg_parser.parse_args(args=arguments)

    tile_bbox = get_bb_from_tile_id(
        args.tile_id, args.auxdata_dirpath, args.s2, args.l8
    )


if __name__ == "__main__":
    sys.exit(main())
