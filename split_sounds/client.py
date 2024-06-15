# SplitUtils
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
import socket

class LSClient:
  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self, hostname, port):
    self.sock.connect((hostname, port))

  def close(self):
    self.sock.close()

  def sendCommand(self, command):
    cmd = command + "\r\n"
    self.sock.sendall(cmd.encode("utf-8"))

  def sendCommandAwaitResponse(self, command):
    cmd = command + "\r\n"
    self.sock.sendall(cmd.encode("utf-8"))
    response = self.sock.recv(8192).decode("utf-8")
    if response.endswith("\r\n"):
      response = response[:-4]
    return response


  def startOrSplit(self):
    self.sendCommand("startorsplit")

  def split(self):
    self.sendCommand("split")

  def unsplit(self):
    self.sendCommand("unsplit")

  def skipSplit(self):
    self.sendCommand("skipsplit")

  def pause(self):
    self.sendCommand("pause")

  def resume(self):
    self.sendCommand("resume")

  def reset(self):
    self.sendCommand("reset")

  def startTimer(self):
    self.sendCommand("starttimer")

  def setGameTime(self, time):
    self.sendCommand("setgametime " + str(time))

  def setLoadingTimes(self, time):
    self.sendCommand("setloadingtimes " + str(time))

  def pauseGameTime(self):
    self.sendCommand("pausegametime")

  def unpauseGameTime(self):
    self.sendCommand("unpausegametime")

  def alwaysPauseGameTime(self):
    self.sendCommand("alwayspausegametime")

  def setComparison(self, comparison):
    self.sendCommand("setcomparison " + str(comparison))

  def switchTo(self, timingMethod):
    self.sendCommand("switchto " + str(timingMethod))

  def setSplitName(self, index, name):
    self.sendCommand("setsplitname " + str(index) + " " + str(name))

  def setCurrentSplitName(self, name):
    self.sendCommand("setcurrentsplitname " + str(name))

  def getDelta(self, comparison=None):
    if comparison != None:
      response = self.sendCommandAwaitResponse("getdelta " + str(comparison))
    else:
      response = self.sendCommandAwaitResponse("getdelta")
    return response

  def getLastSplitTime(self):
    response = self.sendCommandAwaitResponse("getlastsplittime")
    return response

  def getComparisonSplitTime(self):
    response = self.sendCommandAwaitResponse("getcomparisonsplittime")
    return response

  def getCurrentRealTime(self):
    response = self.sendCommandAwaitResponse("getcurrentrealtime")
    return response

  def getCurrentGameTime(self):
    response = self.sendCommandAwaitResponse("getcurrentgametime")
    return response

  def getCurrentTime(self):
    response = self.sendCommandAwaitResponse("getcurrenttime")
    return response

  def getFinalTime(self, comparison=None):
    if comparison != None:
      response = self.sendCommandAwaitResponse("getfinaltime " + str(comparison))
    else:
      response = self.sendCommandAwaitResponse("getfinaltime")
    return response

  def getPredictedTime(self, comparison):
    response = self.sendCommandAwaitResponse("getpredictedtime " + str(comparison))
    return response

  def getBestPossibleTime(self):
    response = self.sendCommandAwaitResponse("getbestpossibletime")
    return response

  def getSplitIndex(self):
    response = self.sendCommandAwaitResponse("getsplitindex")
    return response

  def getCurrentSplitName(self):
    response = self.sendCommandAwaitResponse("getcurrentsplitname")
    return response

  def getPreviousSplitName(self):
    response = self.sendCommandAwaitResponse("getprevioussplitname")
    return response

  def getCurrentTimerPhase(self):
    response = self.sendCommandAwaitResponse("getcurrenttimerphase")
    return response
