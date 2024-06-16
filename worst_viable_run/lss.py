# splitutils
# Copyright (C) 2024  symplicial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Open a livesplit file
def open(filename):
  return ET.parse(filename)

# Write a livesplit file
def write(lss, filename):
  lss.write(filename)

# Parse a livesplit file
def parse(lss):
  root = lss.getroot()

  # Generate a list of attempts
  attemptCount = int(root.find("AttemptCount").text)

  attempts = []
  for i in range(0, attemptCount):
    attempts.append([])

  segments = root.find("Segments")
  for segment in segments:
    history = segment.find("SegmentHistory")
    for i in range(0, attemptCount):
      attemptSegment = history.find(".//Time[@id='" + str(i + 1) + "']")
      if attemptSegment == None:
        attempts[i].append(None)
      else:
        timeTag = attemptSegment.find("RealTime")
        if timeTag == None:
          attempts[i].append(None)
        else:
          time = timeTag.text
          # Precision only up to microseconds
          time = time[:-1] # Kinda hacky, probably should be better about this.
          time_datetime = datetime.strptime(time, "%H:%M:%S.%f")
          time_delta = timedelta(hours=time_datetime.hour, minutes=time_datetime.minute, seconds=time_datetime.second)
          seconds = time_delta.seconds
          attempts[i].append(seconds)

  # Mark resets
  for attempt in attempts:
    lastSegment = -1
    for i in range(0, len(attempt)):
      if attempt[len(attempt) - 1 - i] != None:
        lastSegment = len(attempt) - 1 - i
        break
    if lastSegment < len(attempt) - 1:
      attempt[lastSegment + 1] = "R"

  return attempts

# Write a set of splits to the LSS file
def writeSplits(lss, splits, name):
  root = lss.getroot()
  segments = root.find("Segments")
  i = 0
  for segment in segments:
    splitTimes = segment.find("SplitTimes")
    splitTime = splitTimes.find(".//SplitTime[@name='" + name + "']")
    if splitTime != None:
      splitTimes.remove(splitTime)
    splitTime = ET.Element("SplitTime", {"name": name})
    realTime = ET.Element("RealTime")
    time = timedelta(seconds=splits[i])
    realTime.text = str(time)
    splitTime.append(realTime)
    splitTimes.append(splitTime)
    i += 1
