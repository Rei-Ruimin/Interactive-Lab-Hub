from datetime import datetime

def GetTime():
  return datetime.now().month

def ProcessTime(month):
    if month < 3 or month == 12:
        return 0
    if month > 3 and month < 6:
        return 1
    if month > 6 and month < 9:
        return 2
    else:
        return 3


def GetFruitImage(season, fruit):
  return f"./fruit/{season.lower()}{fruit}.png"


def GetSeasonImage(season):
  return f"./background/{season.lower()}.JPG"

cutoff_start = {
  0: datetime(2023, 12, 1),
  1: datetime(2024, 3, 1),
  2: datetime(2024, 6, 1),
  3: datetime(2024, 9, 1)
}

cutoff_end = {
  0: datetime(2024, 2, 29),
  1: datetime(2024, 5, 31),
  2: datetime(2024, 8, 31),
  3: datetime(2023, 11, 30)
}


def DaysUntil(index):
    seasons = ["Winter", "Spring", "Summer", "Autumn"]
    today = datetime.now()
    next_season = cutoff_start[index]
    time_until = next_season - today
    return f"{time_until.days} Days Until {seasons[index]}"


def DaysLeft(index):
  seasons = ["Winter", "Spring", "Summer", "Autumn"]
  today = datetime.now()
  end_season = cutoff_end[index]
  time_left = end_season - today
  return f"{time_left.days} Days Left in {seasons[index]}"

def Timer(month, seasonIndex):

  if month in [12, 1, 2] and seasonIndex == 0: return DaysLeft(seasonIndex)
  elif month in [3, 4, 5] and seasonIndex == 1: return DaysLeft(seasonIndex)
  elif month in [6, 7, 8] and seasonIndex == 2: return DaysLeft(seasonIndex)
  elif month in [9, 10, 11] and seasonIndex == 3: return DaysLeft(seasonIndex)
  else: return DaysUntil(seasonIndex)