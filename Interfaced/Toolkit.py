#/usr/bin/python3
"""
Toolkit for the SuperMarine Interface
(c) Gabriel St-Pierre-Lemieux
"""

TPM_STR = "\ttransportModel {};\n"
NU_STR  = "\tnu             [0 2 -1 0 0 0 0]  {};\n"
RHO_STR = "\trho            [1 -3 0 0 0 0 0]  {};\n"

def stringNewtonian(rho,nu):
    toPrint = "{\n"
    toPrint += TPM_STR.format("Newtonian")
    toPrint += NU_STR.format(nu)
    toPrint += RHO_STR.format(rho)
    toPrint += "}\n"
    return toPrint


def applyOption(option, template):
    templateFile = open(template,'r')
    lines = templateFile.readlines()
    templateFile.close()
    transformedText = ""
    for line in lines:
        transformedText+= line.format(**option)
    return transformedText

def genSupM(opt):
    # The start of the script
    document = ""
    header = open("./assets/template/supm-header")
    document += "".join(header.readlines())
    header.close()
    # Generate the options
    document += "\nDIVI = [{r}, {theta}, {z}]\n".format(**opt)
    document += "NSEC = {nsec}\n".format(**opt)
    document += "SQRATIO = {sqratio}\n".format(**opt)
    document += "RQUAD = {sqratio}\n".format(**opt)
    document += "SHAFT = {shaft}\n".format(**opt)
    document += "LVLROT = {lvlrot}\n".format(**opt)
    document += "HLAY = {hlay}\n".format(**opt)
    document += "IMPELLERCUT = {impellercut}\n".format(**opt)
    document += "\n"
    # The rest of the script
    tail = open("./assets/template/supm-tail")
    document += "".join(tail.readlines())
    tail.close()
    return document

def genTransport(opt):
    pass

def genVelocity(opt):
    pass

if __name__ == "__main__":
    opt = dict()
    opt["phaseOne"] = stringNewtonian(998, 8.89e-7)
    opt["phaseTwo"] = stringNewtonian(457, 4e-8)
    print("-- Transport Test --")
    print(applyOption(opt, "./assets/template/transportProperties"))

    opt = dict()
    opt["r"] = 10
    opt["theta"] = 10
    opt["z"] = 10
    opt["nsec"] = 4
    opt["sqratio"] = 0.62
    opt["lvlrot"]= "[0, 0, 0, 0]"
    opt["hlay"]  = "[1, 1, 1, 1]"
    opt["shaft"] = "[0, 0, 0, 0]"
    opt["rquad"] = "[0.1,0.2,0.3]"
    opt["impellercut"] = "[0]"

    print("-- SuperMarine Generation Test --")
    print(genSupM(opt))