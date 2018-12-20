# idea : replace actual su_mo_sparse_code.cha by newest old_chas/su_mo_year-mo-da.cha



import sys
import os
import re
from shutil import copy, move
import subprocess
from datetime import date, datetime

def get_latest(old_chas_dir):
    year = 0
    month = 0
    day = 0
    hour = 100
    latest = ""
    for cha_file in sorted(os.listdir(old_chas_dir)):
        if re.match(r'^[0-9][0-9]_[0-9][0-9]_sparse_code_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9]+.cha$', cha_file):
            cur_year = cha_file[18:22]
            cur_month = cha_file[23:25]
            cur_day = cha_file[26:28]
            cur_hour = cha_file[29:31]
            # print(cha_file, latest, cur_hour, hour)
            if (int(cur_year)>year or (int(cur_year)==year and int(cur_month)>month) or (int(cur_year)==year and int(cur_month)==month and int(cur_day)>day) or (int(cur_year)==year and int(cur_month)==month and int(cur_day)==day and int(cur_hour)<hour)):
            #if int(cur_year)>year and int(cur_month)>month and int(cur_day)>day and int(cur_hour)<hour: # last part to get version without ID
                latest = cha_file
                year = int(cur_year)
                month = int(cur_month)
                day = int(cur_day)
                hour = int(cur_hour)
                # print(year, month, day)
    print("latest", latest)
    return latest


def apply_script(script, file_to_process):
    cmd = ["sudo", "python", script, file_to_process]
    subprocess.call(cmd)

def process_subject_month_files(annot_folder_full, script):
    print(annot_folder_full)
    if os.path.isdir(annot_folder_full):
        # print("yep")
        for annot_file in os.listdir(annot_folder_full):
            annot_file_full = os.path.join(annot_folder_full, annot_file)
            if annot_file_full.endswith(".cha") and os.path.isfile(annot_file_full):
                # to change for actual copying file+script
                #print("cur", annot_file_full)
                today = date.today()
                hour = datetime.now()
                today_str = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
                hour_str = str(hour.hour)+'-'+str(hour.minute)+'-'+str(hour.second)
                now_str = today_str + '-' + hour_str
                old_version_name = annot_folder_full+"/old_chas/"+annot_file[:-4]+'_'+now_str+".cha"
                newest = get_latest(annot_folder_full+"/old_chas/")
                tmp = os.path.join(annot_folder_full, newest)
                #print("old", old_version_name)

                copy(os.path.join(annot_folder_full, "old_chas", newest), os.path.join(annot_folder_full, newest))
                move(annot_file_full, old_version_name)
                move(os.path.join(annot_folder_full, newest), annot_file_full)
                #apply_script(script, annot_file_full)

def month_should_be_processed(age_folder, month):
    if month[0]=='-' and age_folder[0:2] not in month:
        return True
    if month[0]=='+' and age_folder[0:2] in month:
        return True
    return False

def process_subject_files(subject_folder_full, month, script):
    ages = os.listdir(subject_folder_full)
    ages.sort()
    for age_folder in ages:
        # function to check folder name?
        if re.match(r'^[0-9][0-9]_[0-9][0-9]$', age_folder):
            # specific age or all ages
            # print(month, age_folder)
            if (month and age_folder[3:5] in month) or not month:
                age_folder_full = os.path.join(subject_folder_full, age_folder)
                annot_folder_full = os.path.join(age_folder_full, "Home_Visit/Coding/Audio_Annotation/")
                process_subject_month_files(annot_folder_full, script)


def should_be_processed(subject_folder, subject):
    if subject[0]=='-' and subject_folder[0:2] not in subject:
        return True
    if subject[0]=='+' and subject_folder[0:2] in subject:
        return True
    return False

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
            # print(subject_folder, subject, int(subject_folder[0:2]) in subject)
            # specific subject to process or all subjects
            # print(not subject, subject)
            if (subject and subject_folder[0:2] in subject) or not subject:

                subject_folder_full = os.path.join(sub_path, subject_folder)
                if not os.path.isdir(subject_folder_full):
                    # print("npe")
                    continue
                process_subject_files(subject_folder_full, month, script)





if __name__ == "__main__":
    sub_path = sys.argv[1]

    subject = sys.argv[2]
    if subject == "--all":
        subject = ''
    else:
        subject = subject.split('_')
    month = sys.argv[3]
    if month == "--all":
        month = ''
    else:
        month = month.split('_')
    # script = ''
    process_files(sub_path, '', subject, month)
