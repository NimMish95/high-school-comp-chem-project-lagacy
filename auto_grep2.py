import subprocess
import os



def Read_and_Generate_txt():
    result_err = subprocess.check_output(["tail *.log"],shell=True)
    result_GE = subprocess.check_output(["grep 'Free Energies' *.log"],shell=True, stderr=subprocess.STDOUT)
    result_EE = subprocess.check_output(["grep 'SCF Done' *.log"],shell=True, stderr=subprocess.STDOUT)

    path = os.path.basename(os.getcwd())

    f = open(path + "_Result.txt","w")

    context = ""

    f.write("<log file condition>\n\n")

    output_data = {}

    file_err_check = result_err.split("==> ")
    file_err_check.pop(0)
    for check in file_err_check:
        file_name = check.split(" <==")[0]

        if "Normal termination of Gaussian 16" in check:
            f.write(file_name + "\t\t\tSuccess\n")
            output_data[file_name] = ["Success",'','']

        else:
            line = -7
            Error_reason = check.split("\n")[line]
            while Error_reason == "":
                line -= 1
                Error_reason = check.split("\n")[line]
            f.write(file_name + "\t\t\tError:\t" + Error_reason + "\n")
            output_data[file_name] = ["Error"]

    f.write("\n\n\n\n")


    f.write("<Gibbs Free Energies>\n\n" + result_GE + "\n\n\n\n")
    result_GE = result_GE.split("\n")
    for result in result_GE:
        result = result.split(": Sum of electronic and thermal Free Energies=")
        try:
            output_data[result[0]][1] = result[1]
        except:
            continue
        


    EEs = {}
    result_EE = result_EE.split("\n")
    for result in result_EE:
        result = result.split(": SCF Done:")
        if len(result) == 1:
            continue
        EEs[result[0]] = result[1]
        result[1] = result[1].split("=")[1].split("A.U.")[0].split("a.u.")[0]
        try:
            output_data[result[0]][2] = result[1]
        except:
            continue

    f.write("<Electronic Energies>\n\n")

    for EE in EEs:
        f.write(EE + EEs[EE] + "\n")

    f.close()

    return output_data


def Universal_Generate_csv(data):

    path = os.path.basename(os.getcwd())

    f = open(path + "_Result.csv","w")
    f.write("'file name','S/E','Gibbs Energy','Electronic Energy'\n")
    for i in data:
        if len(data[i]) == 3:
            f.write(i + "," + data[i][0] + "," + data[i][1] + "," + data[i][2] + '\n')
        else:
            f.write(i + "," + data[i][0] + '\n')
def Kinetics_simulation_Generate_csv(data):
    path = os.path.basename(os.getcwd())

    f = open(path + "_Result.csv","w")
    f.write("file name,S/E,Gibbs Energy,Electronic Energy\n")
    distances = []
    Distance_to_File_name = {}
    for i in data:
        distance = float(i.split("_")[1].rstrip(".log"))
        distances.append(distance)
        Distance_to_File_name[distance] = i
    distances.sort()
    
    
    for distance in distances:
        i = data[Distance_to_File_name[distance]]
        if len(i) == 3:
            f.write(str(distance) + "," + i[0] + "," + i[1] + "," + i[2] + '\n')
        else:
            f.write(str(distance) + "," + i[0] + '\n')

data = Read_and_Generate_txt()
Kinetics_simulation_Generate_csv(data)



