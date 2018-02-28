#!/usr/bin/python3
# coding=utf-8
# Ready Up!
# OpenFOAM preparation script.
# Author: Gabriel Lemieux
import os
import subprocess as sp
import re
import time
from shutil import rmtree

CASE_DIR = "./"
PROCESSOR = 1
SOLVER = "None"

RED = "\033[31m"
GREEN = "\033[32m"
STD = "\033[0m"


def continueq(stepstring):
    """
    Ask if the user want to continue
    the execution of the script.

    :param stepstring: The string refering to the step
    :return: None
    """
    print(stepstring, "\nContinue (y/n)?")
    inp = input()
    if not (inp == "y" or inp == "yes"):
        quit()


def execute(protocol):
    """
    Execute each steps of the
    presented protocol.

    :param protocol: Is an array of instructions following this template:
                        ["String to print",["command","arg1","arg2",...]]
    :return: None
    """
    # Setup log file
    logfile = open("setup.log", "a")
    errfile = open("setup_err.log", "a")

    # Loop each instructions of the protocol
    for instruction in protocol:
        # Start instruction and
        # wait the exit condition
        print(instruction[0], end='', flush=True)
        rc = sp.Popen(instruction[1], stdout=logfile.fileno(), stderr=errfile.fileno())
        return_results = None

        # The wait loop
        # it's only test each second (to free up computing time)
        symboles = ["•", "0", "·"]
        itt = 0
        while return_results is None:
            print("...", symboles[itt % 3], end="\b" * 5, flush=True)
            time.sleep(1)
            return_results = rc.poll()
            itt += 1
        # Exit condition give an error
        if return_results != 0:
            print(" --  " + RED + "FAILED" + STD)
            continueq("The last command failed... Does you wish to continue anyway?")
        # Exit condition give no error
        else:
            print(" --  " + GREEN + "DONE" + STD)


def remove(folder, regex):
    """
    Remove the file matching regex in the specified folder
    :param folder: folder relative path from scripts
    :param regex:  regular expression
    :return:
    """
    folder = folder.strip("/")
    base = os.listdir(folder)
    for file in base:
        if re.match(regex, file):
            if not os.path.isdir(folder + "/" + file):
                print("\033[31mRemoving:\033[0m ", folder + "/" + file)
                os.remove(folder + "/" + file)


def remove_processor():
    base = os.listdir(CASE_DIR)
    for file in base:
        if re.match("processor[0-9]*", file):
            print("\033[31mRemoving:\033[0m ", file)
            rmtree(file)


def remove_time_step():
    base = os.listdir(CASE_DIR)
    for file in base:
        if re.match("^[0-9]+\.?[0-9]*$", file):
            print(RED + "Removing: " + STD, file)
            rmtree(file)


def remove_pycache():
    """
    Remove pycache directory
    :return: None
    """
    base = os.listdir(CASE_DIR)
    for file in base:
        if re.match("^__pycache__$", file):
            print(RED + "Removing: " + STD, file)
            rmtree(file)


def main():
    # Cleaning
    print("\n" + "*" * 10)
    print("\033[32m Cleaning \033[0m")
    print("*" * 10)

    # Clean the base directorie
    to_remove = [
        "run.sh",
        ".*.log$"
    ]

    for elem in to_remove:
        remove("./", elem)

    # Remove Time Steps and Processor Dir
    remove_time_step()
    remove_processor()

    # Clean polymesh
    remove("./constant/polyMesh", ".*")

    # Meshing protocol
    # EVERYTING IS IN CENTIMETER IN THIS STEP
    print("\n" + "*" * 10)
    print("\033[32m Meshing \033[0m")
    print("*" * 10)
    protocol = [
        ["Dummy 0 file", ["mkdir", "0"]],
        ["Generate Mesh (Step 1)", ["python3.5", "./superMarine-0.3b.py"]],
        ["Generate Mesh (Step 2)", ["blockMesh"]]
    ]

    execute(protocol)
    # NOW EVERYTHING IS IN METER
    # MRF meshing protocol

    # Preparation protocol
    print("\n" + "*" * 10)
    print("Pre-processing")
    print("*" * 10)

    remove_time_step()
    remove_processor()

    protocol = [
        ["Set Zones", ["topoSet"]],
        ["Update cellzones", ["setsToZones", "-noFlipMap"]],
        ["Copies of the starting parameters", ["cp", "-R", "init", "0"]],
        ["Set the alpha fields", ["setFields"]],
        ["Decompose the case", ["decomposePar"]]
    ]
    execute(protocol)


if __name__ == '__main__':
    main()
