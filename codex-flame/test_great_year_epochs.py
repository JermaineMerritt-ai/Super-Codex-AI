# test_great_year_epochs.py
# Test script to demonstrate Great Year Rite across different millennia
import datetime

def epoch_key(dt):
    # Define epochs by millennia
    return f"{(dt.year // 1000) * 1000}-{((dt.year // 1000) * 1000) + 999}"

# Test different historical and future epochs
test_years = [
    1000,  # First millennium CE
    1500,  # Late medieval
    1999,  # End of second millennium
    2000,  # Start of third millennium
    2025,  # Current year
    2500,  # Mid third millennium
    2999,  # End of third millennium
    3000,  # Start of fourth millennium
    3999,  # End of fourth millennium
    4000,  # Start of fifth millennium
]

print("👑 Great Year Rite - Millennial Epoch Proclamations 👑\n")

for year in test_years:
    test_date = datetime.datetime(year, 6, 21)  # Summer solstice
    epoch = epoch_key(test_date)
    status = "🔥 CURRENT EPOCH" if year == 2025 else "📜 Historical/Future"
    print(f"Year {year:4d}: Epoch {epoch} {status}")

print(f"\n✨ Current Great Year Epoch: {epoch_key(datetime.datetime.now())}")
print("🌟 Crown of the Third Millennium: 2000-2999 CE")