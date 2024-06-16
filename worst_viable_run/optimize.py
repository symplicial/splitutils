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
import math
from numpy import convolve
from scipy import optimize
from datetime import timedelta

import lss

class TimeDistribution:
  def __init__(self, start, frequencies):
    self.start = start
    self.frequencies = frequencies

  def D_l(self, t):
    start = self.start
    frequencies = []
    for i in range(0, min(len(self.frequencies), math.floor(t) - self.start)):
      frequencies.append(self.frequencies[i])
    return TimeDistribution(start, frequencies)

  def D_le(self, t):
    start = self.start
    frequencies = []
    for i in range(0, min(len(self.frequencies), math.floor(t) - self.start + 1)):
      frequencies.append(self.frequencies[i])
    return TimeDistribution(start, frequencies)

  def D_g(self, t):
    start = max(math.ceil(t), self.start)
    frequencies = []
    for i in range(max(math.ceil(t) - self.start, 0), len(self.frequencies)):
      frequencies.append(self.frequencies[i])
    return TimeDistribution(start, frequencies)

  def D_ge(self, t):
    start = max(math.ceil(t) - 1, self.start)
    frequencies = []
    for i in range(max(math.ceil(t) - self.start - 1, 0), len(self.frequencies)):
      frequencies.append(self.frequencies[i])
    return TimeDistribution(start, frequencies)

  def E(self, f):
    result = 0
    for i in range(0, len(self.frequencies)):
      result += self.frequencies[i] * f(self.start + i)
    return result


def fillResets(attempts, resetTimes):
  for attempt in attempts:
    for i in range(0, len(attempt)):
      if attempt[i] == "R":
        attempt[i] = resetTimes[i]

def trialsFromAttempts(attempts):
  trials = []
  for i in range(0, len(attempts[0])):
    trials.append([])
  for attempt in attempts:
    for i in range(0, len(attempts[0])):
      if attempt[i] != None:
        trials[i].append(attempt[i])
  return trials

def distributionFromTrials(trials):
  best = 0
  worst = 0
  if len(trials) > 0:
    best = trials[0]
    worst = trials[0]
    for t in trials:
      if t <= best:
        best = t
      if t >= worst:
        worst = t

  count = len(trials)
  start = math.floor(best)
  frequencies = []
  for i in range(0, math.ceil(worst) - start + 1):
    frequencies.append(0)
  for t in trials:
    index = math.floor(t) - start
    frequencies[index] += 1 / float(count)

  return TimeDistribution(start, frequencies)

def combineDistributions(a, b):
  start = a.start + b.start
  frequencies = []
  if len(a.frequencies) > 0 and len(b.frequencies) > 0:
    frequencies = convolve(a.frequencies, b.frequencies)
  return TimeDistribution(start, frequencies)

# The value we want to minimize is the expected time to reach the target. This
# can be calculated as the expected length of an attempt divided by the
# probability of success for one attempt.
def P_success(distributions, splits):
  d = distributions[0].D_le(splits[0])
  for i in range(1, len(splits)):
    d = combineDistributions(d, distributions[i]).D_le(splits[i])
  return d.E(lambda t: 1.0)

def expected_attempt_length(distributions, splits):
  result = 0.0

  # Calculate the expected length when we fail on a given segment
  for k in range(0, len(splits)):
    if k == 0:
      d = distributions[0].D_g(splits[0])
      result += d.E(lambda t: t)
    else:
      d = distributions[0].D_le(splits[0])
      for i in range(1, k):
        d = combineDistributions(d, distributions[i]).D_le(splits[i])
      d = combineDistributions(d, distributions[k]).D_g(splits[k])
      result += d.E(lambda t: t)

  # Calculate the expected length of a success
  d = distributions[0].D_le(splits[0])
  for i in range(1, len(splits)):
    d = combineDistributions(d, distributions[i]).D_le(splits[i])
  result += d.E(lambda t: t)

  return result

def expected_time(distributions, splits):
  P = P_success(distributions, splits)
  if P == 0:
    return float("inf")
  else:
    return expected_attempt_length(distributions, splits) / P

def segmentsToSplits(segments):
  splits = []
  for j in range(0, len(segments)):
    split = 0
    for i in range(0, j + 1):
      split += segments[i]
    splits.append(split)
  return splits

def splitsToSegments(splits):
  segments = []
  for i in range(0, len(splits)):
    if i == 0:
      segments.append(splits[i])
    else:
      segments.append(splits[i] - splits[i - 1])
  return segments

def splitsOK(splits):
  for i in range(0, len(splits) - 1):
    if splits[i] > splits[i + 1]:
      return False
  return True


# Use balanced splits as our starting point.
def balanced(distributions, target):
  sum_of_best = 0
  for j in range(0, n_segments):
    sum_of_best += distributions[j].start
  segment_times = []
  for j in range(0, n_segments):
    segment_times.append((distributions[j].start * target) / sum_of_best)
  return segmentsToSplits(segment_times)

def bestSegmentsFromAttempts(attempts):
  best = [9999999999999] * len(attempts[0])
  for attempt in attempts:
    for i in range(0, len(attempt)):
      if attempt[i] != "R" and attempt[i] != None and attempt[i] < best[i]:
        best[i] = attempt[i]
  return best

def bestSegments(trials):
  best = [9999999999999] * len(trials)
  for i in range(0, len(trials)):
    trial = trials[i]
    for time in trial:
      if time < best[i]:
        best[i] = time
  return best

def resetTimes(best, offset):
  resetTimes = []
  for i in range(0, len(best)):
    resetTimes.append(best[i] + offset)
  return resetTimes

def removeLastSegment(splits):
  return splits[:-1]

def addLastSegment(splits, lastSegment):
  return [*splits, float(lastSegment)]

def expectedTimeLastSegmentRemoved(distributions, lastSegment):
  def computeExpectedTime(splits):
    return expected_time(distributions, addLastSegment(splits, lastSegment))
  return computeExpectedTime

def makeBounds(trials, target):
  # Lower bound is sum of best and upper bound is the target time minus the sum of best for all following segments.
  best = bestSegments(trials)
  bounds = []
  for i in range(0, len(trials) - 1):
    lowerBound = 0
    for j in range(0, i + 1):
      lowerBound += best[j]
    upperBound = target
    for j in range(i + 1, len(trials)):
      upperBound -= best[j]
    bounds.append((lowerBound, upperBound))
  return bounds

def findBestSplits(lssFile, target, resolution, resetDelay):
  attempts = lss.parse(lssFile)
  n_segments = len(attempts[0])
  fillResets(attempts, resetTimes(bestSegmentsFromAttempts(attempts), 45))
  trials = trialsFromAttempts(attempts)

  distributions = []
  for i in range(0, n_segments):
    distribution = distributionFromTrials(trials[i])
    distributions.append(distribution)

  # Run the optimization process.
  targetSeconds = target.seconds
  result = optimize.dual_annealing(expectedTimeLastSegmentRemoved(distributions, targetSeconds), makeBounds(trials, targetSeconds))
  best_splits = addLastSegment(result.x, targetSeconds)

  return best_splits
