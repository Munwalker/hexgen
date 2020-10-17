import math
import random


class Month:

    def __init__(self, ordinal, num_days, day_length):
        self.ordinal = ordinal
        self.num_days = num_days
        self.day_length = day_length

    def __repr__(self):
        return f"<Month ordinal={self.ordinal} " \
               f"num_days={self.num_days} " \
               f"day_length={self.day_length}>"


class Calendar:

    def __init__(self, year_length, day_length, month_length_target=None):
        self.year_length = year_length
        self.day_length = day_length

        self.months = []

        # determine the number of months
        # split the year_length into twelve months with an integer number of days
        # each month should have around 30 days
        if not month_length_target:
            if year_length > 35:
                month_length_target = random.randint(25, 35)
            else:
                month_length_target = year_length / 2
        # print(f"Target length of month: {month_length_target}")

        num_months = round(year_length / month_length_target)
        # print(f"Number of months: {num_months}")
        even_split = year_length / num_months
        # print(f"Length of each month if split evenly: {even_split}")

        days_left = year_length
        even_split = math.floor(even_split)
        for num in range(1, num_months + 1):
            # print(days_left, '-', even_split, days_left - even_split, '<', 0)
            if days_left - even_split < even_split:
                num_days = days_left
            else:
                num_days = even_split
            self.months.append(Month(num, num_days, day_length))
            days_left -= even_split

        # for month in self.months:
        #     print(f"{month}")
        # print(f"total: {sum([x.num_days for x in self.months])}")


#
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# echo = pp.pprint
#
# def generate_calendar(len_year, len_day):
#     """
#     len_year = (int) length of year in Earth days
#     len_day = (int) length of day in Earth hours
#     """
#     print("Generating calendar")
#     calendar = Calendar(len_year, len_day)
#     echo(calendar.months)
#     return calendar
#
#
# generate_calendar(365, 24)
# generate_calendar(231, 34)
