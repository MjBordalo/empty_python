from datetime import datetime

def write_freeze_ram_file(folder="/tmpfolder/",file="freeze_cameraA.txt"):

        src=folder+file
        with open(src, mode='w') as file:
                file.write(str( datetime.now()))
