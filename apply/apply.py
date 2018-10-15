
import sys
import os
import re
from shutil import copy
import subprocess
from datetime import date

def apply_script(script, file_to_process):
    cmd = ["sudo", "python", script, file_to_process]
    subprocess.call(cmd)

def process_subject_month_files(annot_folder_full, script):
    if os.path.isdir(annot_folder_full):
        for annot_file in os.listdir(annot_folder_full):
            annot_file_full = os.path.join(annot_folder_full, annot_file)
            if annot_file_full.endswith(".cha") and os.path.isfile(annot_file_full):
                # to change for actual copying file+script
                print(annot_file_full)
                today = date.today()
                today_str = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
                old_version_name = annot_folder_full+"/old_chas/"+annot_file[:-4]+'_'+today_str+".cha"
                print(old_version_name)
                copy(annot_file_full, old_version_name)
                apply_script(script, annot_file_full)

def process_subject_files(subject_folder_full, month, script):
    ages = os.listdir(subject_folder_full)
    ages.sort()
    for age_folder in ages:
        # function to check folder name?
        if re.match(r'^[0-9][0-9]_[0-9][0-9]$', age_folder):
            # specific age or all ages
            if (month and age_folder[3:5]==month) or not month:
                age_folder_full = os.path.join(subject_folder_full, age_folder)
                annot_folder_full = os.path.join(age_folder_full, "Home_Visit/Coding/Audio_Annotation/")
                process_subject_month_files(annot_folder_full, script)




def process_files(sub_path, script, subject, month):
    if not os.path.isdir(sub_path):
        print "{} is not a directory".format(sub_path)
        return
    # Get all the directories in Subject_Files
    children = os.listdir(sub_path)
    # order them by number
    children.sort()
    for subject_folder in children:
        if subject_folder.isdigit():
            # specific subject to process or all subjects
            if (subject and subject_folder[0:2]==subject) or not subject:
                subject_folder_full = os.path.join(sub_path, subject_folder)
                if not os.path.isdir(subject_folder_full):
                    continue
                process_subject_files(subject_folder_full, month, script)





if __name__ == "__main__":
    sub_path = sys.argv[1]
    script = sys.argv[2]

    subject = sys.argv[3]
    if subject == "--all":
        subject = ''
    month = sys.argv[4]
    if month == "--all":
        month = ''

    process_files(sub_path, script, subject, month)
