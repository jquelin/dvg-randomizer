#
# This file is part of dvg-randomizer.
#
# dvg-randomizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# dvg-randomizer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dvg-randomizer. If not, see
# <https://www.gnu.org/licenses/>.
#

import pytest

from aircraft import Aircraft
from boardgame import Boardgame

bg = Boardgame("TestGame", "TG", ["track1", "track2"])

# Test suite for Aircraft

def test_aircraft_initialization():
    aircraft = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF",
        name     = "F-16",
        year_in  = 1978,
        year_out = 2005,
        cost_s   = 10,
        cost_m   = 20,
        cost_l   = 30,
        role     = "Fighter"
    )

    assert aircraft.boardgame == bg
    assert aircraft.box       == "core"
    assert aircraft.service   == "USAF"
    assert aircraft.services  == ["USAF"]
    assert aircraft.name      == "F-16"
    assert aircraft.year_in   == 1978
    assert aircraft.year_out  == 2005
    assert aircraft.cost_s    == 10
    assert aircraft.cost_m    == 20
    assert aircraft.cost_l    == 30
    assert aircraft.role      == "Fighter"

def test_aircraft_initialization_with_no_year_out():
    aircraft = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF",
        name     = "F-16",
        year_in  = 1978,
        year_out = None,
        cost_s   = 10,
        cost_m   = 20,
        cost_l   = 30,
        role     = "Fighter"
    )

    assert aircraft.year_out == 9999  # Default value for year_out when None is provided

def test_aircraft_id():
    aircraft = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF",
        name     = "F-16",
        year_in  = 1978,
        year_out = 2005,
        cost_s   = 10,
        cost_m   = 20,
        cost_l   = 30,
        role     = "Fighter"
    )

    expected_id = "TG-USAF-F-16"
    assert aircraft.id() == expected_id

def test_aircraft_lt():
    aircraft1 = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF",
        name     = "F-16",
        year_in  = 1978,
        year_out = 2005,
        cost_s   = 10,
        cost_m   = 20,
        cost_l   = 30,
        role     = "Fighter"
    )

    aircraft2 = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF",
        name     = "F-15",
        year_in  = 1976,
        year_out = 2005,
        cost_s   = 15,
        cost_m   = 25,
        cost_l   = 35,
        role     = "Fighter"
    )

    assert (aircraft2 < aircraft1) is True  # F-15 < F-16
    assert (aircraft1 < aircraft2) is False

def test_aircraft_repr():
    aircraft = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF",
        name     = "F-16",
        year_in  = 1978,
        year_out = 2005,
        cost_s   = 10,
        cost_m   = 20,
        cost_l   = 30,
        role     = "Fighter"
    )

    expected_repr = "TG-USAF-F-16 (Fighter) [1978-2005]"
    assert repr(aircraft) == expected_repr

def test_aircraft_services_with_multiple_services():
    aircraft = Aircraft(
        bg       = bg,
        box      = "core",
        service  = "USAF+USN",
        name     = "F-4 Phantom",
        year_in  = 1960,
        year_out = 1996,
        cost_s   = 12,
        cost_m   = 22,
        cost_l   = 32,
        role     = "Multirole"
    )

    assert aircraft.services == ["USAF", "USN"]  # Split services by '+'
