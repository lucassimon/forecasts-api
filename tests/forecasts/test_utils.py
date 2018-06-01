# -*- coding: utf-8 -*-
# Python
import datetime

# Third

import pytest

# Apps
from apps.forecasts.utils import convert_period_to_time, check_period_is_valid


class TestConvertPeriodToTime:

    def test_convert_time_success(self):
        time = convert_period_to_time("18:30")
        assert time == datetime.time(18, 30)


class TestCheckPeriodIsValid:
    def test_period_is_valid(self):
        period = datetime.time(11, 50)

        start = "01:30"
        end = "15:30"
        assert check_period_is_valid(start, period, end)
