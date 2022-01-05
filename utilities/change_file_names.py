import os

path = os.chdir(r'C:\Smart_Food_Keeper\dataset_papaya\unripe_papaya')


def main(PATH,new_name):

    path_to_iterate = PATH
    cant_images_to_rename = 0

    for file in os.listdir(path_to_iterate):
        new_file = new_name +"_{}.jpg".format(cant_images_to_rename)
        os.rename(file, new_file)

        cant_images_to_rename = cant_images_to_rename + 1

    return new_file

if __name__ == '__main__':

    new_name_1 = "unripe_pineapple"
    new_name_2 = "ripe_pineapple"
    new_name_3 = "unripe_papaya"
    new_name_4 = "ripe_papaya"    
    
    parameter = main(path,new_name_3)

    print("[*] Renaming files...")
    print(parameter)
    print("[X] Files were renamed succesfuly")


