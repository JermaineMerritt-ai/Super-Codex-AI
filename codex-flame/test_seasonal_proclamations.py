# test_seasonal_proclamations.py
# Test script to demonstrate seasonal proclamations throughout the year
import datetime

def season_proclamation(dt):
    month, day = dt.month, dt.day
    if month == 12 and day >= 21: return "Winter Solstice Proclamation: Endurance and Renewal"
    if month == 3 and day >= 20: return "Spring Equinox Proclamation: Rebirth and Expansion"
    if month == 6 and day >= 21: return "Summer Solstice Proclamation: Radiance and Abundance"
    if month == 9 and day >= 22: return "Autumn Equinox Proclamation: Harvest and Remembrance"
    return "Daily Flame Invocation: Continuity and Stewardship"

# Test seasonal dates
test_dates = [
    datetime.date(2025, 3, 20),   # Spring Equinox
    datetime.date(2025, 6, 21),   # Summer Solstice  
    datetime.date(2025, 9, 22),   # Autumn Equinox
    datetime.date(2025, 12, 21),  # Winter Solstice
    datetime.date(2025, 11, 10),  # Regular day (today)
    datetime.date(2025, 7, 15),   # Regular summer day
    datetime.date(2025, 1, 15),   # Regular winter day
]

print("🔥 Eternal Flame Seasonal Proclamations Test 🔥\n")

for test_date in test_dates:
    proclamation = season_proclamation(test_date)
    print(f"📅 {test_date.strftime('%B %d, %Y')}: {proclamation}")

print(f"\n✨ Current Date ({datetime.date.today()}): {season_proclamation(datetime.date.today())}")