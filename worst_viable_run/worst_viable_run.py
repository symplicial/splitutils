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
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import shutil
from datetime import datetime, timedelta
import threading

import lss
import optimize as opt

# Create the window.
window = Tk()
window.title("Worst Viable Run Split Generator")
window.geometry("640x480")

# File Select
lssFileLabel = Label(window, text="LSS File: ")
lssFileLabel.grid(column=0, row=0, sticky=W)

window.lssFilename = "---"
lssFilenameLabel = Label(window, text=window.lssFilename)
lssFilenameLabel.grid(column=1, row=0, sticky=E)

def selectFile():
  window.lssFilename = filedialog.askopenfilename()
  lssFilenameLabel["text"] = window.lssFilename

lssFileSelectButton = Button(window, text="Select File", command=selectFile)
lssFileSelectButton.grid(column=2, row=0)

# Target Time
targetTimeLabel = Label(window, text="Target Time: ")
targetTimeLabel.grid(column=0, row=1, sticky=W)

targetTimeVar = StringVar(value="---")
targetTime = Entry(window, textvariable=targetTimeVar)
targetTime.grid(column=1, row=1, sticky=E)

# Comparison Name
comparisonNameLabel = Label(window, text="Comparison Name: ")
comparisonNameLabel.grid(column=0, row=2, sticky=W)

comparisonNameVar = StringVar(value="Reset")
comparisonName = Entry(window, textvariable=comparisonNameVar)
comparisonName.grid(column=1, row=2, sticky=E)

# Resolution
resolutionLabel = Label(window, text="Resolution: ")
resolutionLabel.grid(column=0, row=3, sticky=W)

resolution = Combobox(window, state="readonly", values=("0.01s", "0.1s", "1s", "5s", "10s"))
resolution.current(2)
resolution.grid(column=1, row=3, sticky=E)

# Reset Delay
resetDelayLabel = Label(window, text="Reset Delay: ")
resetDelayLabel.grid(column=0, row=4, sticky=W)

resetDelayVar = StringVar(value="5")
resetDelay = Entry(window, textvariable=resetDelayVar)
resetDelay.grid(column=1, row=4, sticky=E)

# Optimize Button
optimizeProgressBar = Progressbar(mode="indeterminate")
optimizeProgressBar.grid(column=0, row=5, sticky=W)

optimizeResult = [None, None]

def optimizeMain(result):
  # Before doing anything, copy the LSS file to a backup.
  try:
    shutil.copyfile(window.lssFilename, window.lssFilename + ".bak")
  except:
    result[0] = False
    result[1] = "Error creating backup copy."
    return

  # Open the LSS file.
  try:
    lssFile = lss.open(window.lssFilename)
  except:
    result[0] = False
    result[1] = "Error opening LSS file."
    return

  # Get parameters
  formats = ["%H:%M:%S.%f", "%H:%M:%S", "%M:%S.%f", "%M:%S", "%S.%f", "%S"]
  target_datetime = None
  for f in formats:
    try:
      target_datetime = datetime.strptime(targetTime.get(), f)
      break
    except:
      continue
  if target_datetime == None:
    result[0] = False
    result[1] = "Invalid target time."
    return
  target_delta = timedelta(hours=target_datetime.hour, minutes=target_datetime.minute, seconds=target_datetime.second)

  resolutions = [0.01, 0.1, 1.0, 5.0, 10.0]
  timeResolution = resolutions[resolution.current()]

  try:
    delay = float(resetDelay.get())
  except:
    result[0] = False
    result[1] = "Invalid reset delay."
    return

  # Optimize splits.
  try:
    optimized = opt.findBestSplits(lssFile, target_delta, timeResolution, delay)
  except:
    result[0] = False
    result[1] = "Error optimizing splits."
    return

  # Write the results.
  try:
    lss.writeSplits(lssFile, optimized, comparisonNameVar.get())
    lss.write(lssFile, window.lssFilename)
  except:
    result[0] = False
    result[1] = "Error writing splits to LSS file."
    return

  result[0] = True
  result[1] = "Splits succesfully optimized."

def lockInputs():
  lssFileSelectButton.config(state='disabled')
  targetTime.config(state='disabled')
  comparisonName.config(state='disabled')
  resolution.config(state='disabled')
  resetDelay.config(state='disabled')
  optimizeButton.config(state='disabled')

def unlockInputs():
  lssFileSelectButton.config(state='enabled')
  targetTime.config(state='enabled')
  comparisonName.config(state='enabled')
  resolution.config(state='enabled')
  resetDelay.config(state='enabled')
  optimizeButton.config(state='enabled')

def optimize():
  lockInputs()
  optimizeProgressBar.start()

  backgroundThread = threading.Thread(target=optimizeMain, args=(optimizeResult,))
  backgroundThread.start()

  checkProgress(backgroundThread)

def checkProgress(bg):
  if bg.is_alive():
    window.after(100, checkProgress, (bg))
  else:
    # Computation finished. Unlock everything and report the result.
    unlockInputs()
    optimizeProgressBar.stop()
    success = optimizeResult[0]
    message = optimizeResult[1]
    if success:
      messagebox.showinfo("Success!", message)
    else:
      messagebox.showerror("Error", message)

optimizeButton = Button(window, text="Optimize", command=optimize)
optimizeButton.grid(column=2, row=5, sticky=E)

window.mainloop()
