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
from client import LSClient

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

import sched

c = LSClient()
c.connect("localhost", 16834)

if __name__ == "__main__":
  # Create the window.
  window = Tk()
  window.title("resetty")
  window.geometry("640x480")

  # File select.
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

  # Comparison Name
  comparisonNameLabel = Label(window, text="Comparison Name: ")
  comparisonNameLabel.grid(column=0, row=1, sticky=W)

  comparisonNameVar = StringVar(value="Reset")
  comparisonName = Entry(window, textvariable=comparisonNameVar)
  comparisonName.grid(column=1, row=1, sticky=E)

  # Optimization Algorithm
  algorithmLabel = Label(window, text="Optimization Algorithm: ")
  algorithmLabel.grid(column=0, row=2, sticky=W)

  algorithm = Combobox(window, state="readonly", values=("Dual Annealing (Recommended)", "Basin Hopping", "Differential Evolution", "DIRECT (Not Recommended)"))
  algorithm.current(0)
  algorithm.grid(column=1, row=2, sticky=E)

  # Reset Nonattribution Window
  resetNonattributionLabel = Label(window, text="Reset Nonattribution Window: ")
  resetNonattributionLabel.grid(column=0, row=3, sticky=W)

  resetNonattributionVar = StringVar(value="10")
  resetNonattribution = Entry(window, textvariable=resetNonattributionVar)
  resetNonattribution.grid(column=1, row=3, sticky=E)

  # Decay Mode
  decayModeFrame = Frame(window)
  decayModeFrame.grid(column=0, row=4)

  decayModeLabel = Label(decayModeFrame, text="Decay Mode: ")
  decayModeLabel.grid(column=0, row=0, sticky=E)

  decayMode = Combobox(decayModeFrame, state="readonly", values=("None", "Cutoff", "Smoothstep"))
  decayMode.current(0)
  decayMode.grid(column=1, row=0)

  # Optimize Button
  optimizeProgressBar = Progressbar(mode="indeterminate")
  optimizeProgressBar.grid(column=0, row=5, sticky=W)

  def optimizeMain():
    # Before doing anything, copy the LSS file to a backup.
    shutil.copyfile(window.lssFilename, window.lssFilename + ".bak")

    # Open the LSS file.
    lssFile = lss.open(window.lssFilename)

    # Optimize splits.
    optimized = opt.findBestSplits(lssFile, "dual_annealing", (17 * 60) + 34)

    # Write the results.
    lss.writeSplits(lssFile, optimized, "Reset")
    lss.write(lssFile, window.lssFilename)

  def optimize():
    optimizeProgressBar.start()
    #try:
    #  optimizeMain()
    #  optimizeProgressBar.stop()
    #except Exception as e:
    #  print("Error: " + str(e))
    #else:
    #  print("B")

  optimizeButton = Button(window, text="Optimize", command=optimize)
  optimizeButton.grid(column=2, row=5, sticky=E)

  def update():
    # Get delta. If it's positive, play a sound.
    delta = c.getDelta()
    if len(delta) > 0 and delta[0] != "-":
      print("reset!")
    window.after(1000, update)

  window.after(1000, update)
  window.mainloop()
