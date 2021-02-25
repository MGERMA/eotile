# -*- coding: utf-8 -*-
"""
EO tile

:author: msavinaud
:organization: CS-Group
:copyright: 2021 CS-Group France. All rights reserved.
:license: see LICENSE file.
"""

import logging
from shapely.geometry import Polygon, MultiPolygon

LOGGER = logging.getLogger(__name__)


class EOTile:
    """Class which represent a tile """

    def __init__(self):
        """ Constructor """

        self.ID = None
        self.polyBB = None

    def display(self):
        """ Display the content of a tile"""
        print(self.ID)
        print(self.polyBB)

    def get_bb(self):
        """
        Returns the AABB (axis aligned bounding box) of a tile.

        """
        return self.polyBB.GetEnvelope()

class L8Tile(EOTile):
    """ Class which represent a L8 tile """

    def __init__(self):
        """ Constructor """
        EOTile.__init__(self)

    def display(self):
        """ Display the content of a L8 tile"""
        LOGGER.info("== Tile L8 ==")
        EOTile.display(self)



class S2Tile(EOTile):
    """Class which represent a S2 tile read from Tile_Part file"""

    def __init__(self):
        EOTile.__init__(self)
        self.BB = [0, 0, 0, 0, 0, 0, 0, 0]
        self.poly = None
        self.UL = [0, 0]
        self.SRS = None
        self.NRows = []
        self.NCols = []

    def display(self):
        """ Display the content of tile"""
        LOGGER.info("== S2 Tile ==")
        EOTile.display(self)
        print(self.BB)
        print(self.UL)
        print(self.SRS)
        print(self.NRows)
        print(self.NCols)
        print(self.poly)

    def create_poly_bb(self):
        """ Create the Shapely Polygon from the list of BB corner """
        indices = [[1, 0], [3, 2], [5, 4], [7, 6]]
        # Create polygon
        self.polyBB = Polygon([[float(self.BB[ind[0]]), float(self.BB[ind[1]])] for ind in indices])


    def compute_datetime_point(self, east_pt, west_pt):
        lat = 1 # index of latitudes
        long = 1 - lat
        c1_den = -float(self.BB[east_pt[long]]) + float(self.BB[west_pt[long]]) + 360
        c1_num = 180 - float(self.BB[east_pt[long]])
        coeff1_lat = float(self.BB[west_pt[lat]]) - float(self.BB[east_pt[lat]])
        return float(self.BB[east_pt[lat]]) + c1_num / c1_den * coeff1_lat



    def datetime_cutter(self):
        """ Create the Shapely Polygon from the list of BB corner in the case where it crosses the datetime_line"""
        indices = [[1, 0], [3, 2], [5, 4], [7, 6]]
        # compute latitude of cutting points
        lat = 1 # index of latitudes
        long = 1 - lat
        [a, b, c, d] = indices
        if (abs(float(self.BB[1]) - float(self.BB[3])) > 355.0) and (
            abs(float(self.BB[5]) - float(self.BB[7])) > 355.0
        ): # Case where two segments are of each side of the datetime line
            c1_lat = self.compute_datetime_point(a, b)
            c2_lat = self.compute_datetime_point(d, c)
            # Create east polygon
            east_part = Polygon(
                ([
                    [float(self.BB[indices[0][0]]), float(self.BB[indices[0][1]])],
                    [180, c1_lat],
                    [180, c2_lat],
                    [float(self.BB[indices[3][0]]), float(self.BB[indices[3][1]])]
                ])
            )
            # Create west polygon
            west_part = Polygon(
                ([[-180, c1_lat],
                    [float(self.BB[indices[1][0]]), float(self.BB[indices[1][1]])],
                    [float(self.BB[indices[2][0]]), float(self.BB[indices[2][1]])],
                  [-180, c2_lat]
                ])
            )
        if (abs(float(self.BB[1]) - float(self.BB[3])) > 355.0) and not(
            abs(float(self.BB[5]) - float(self.BB[7])) > 355.0
        ): # Case where only top line is crossed
            pass
            # Case 1
            # TODO
            # Case 2
            # TODO
        if not(abs(float(self.BB[1]) - float(self.BB[3])) > 355.0) and (
                abs(float(self.BB[5]) - float(self.BB[7])) > 355.0
        ):  # Case where only bottom line is crossed
            pass
            # Case 1
            # TODO
            # Case 2
            # TODO
        self.polyBB = MultiPolygon([east_part, west_part])