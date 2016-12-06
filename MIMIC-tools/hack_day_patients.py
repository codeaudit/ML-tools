import argparse
import shelve

from os.path import join as pjoin

from MimicPatient import *
from Utils import *

from pprint import pprint

def read_patients_file(file_name):
    patients     = {}
    mimic_desc    = MimicDesc()
    for split_line in read_mimic_csv(file_name):
        try:
            patient = MimicPatient(mimic_desc, split_line)
            if patient.patient_id in patients:
                print "DUPLICATE OBSERVATIONS FOR PATIENT_ID:", patient.patient_id
            else:
                patients[patient.patient_id] = patient
        except:
            print "ERROR-------- Line", split_line
    return patients


def read_admissions_file(patients, file_name):
    mimic_desc    = MimicDesc()
    for split_line in read_mimic_csv(file_name):
        try:
            adm = MimicAdmission(patients, mimic_desc, split_line)
        except:
            print "ERROR-------- Line", split_line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program reads the \
                 MIMIC Patient files, and converts them to shelve format.')
    parser.add_argument("-dir", "--MIMIC3_directory", \
                        default='/data/ml2/MIMIC3/',
                        help="Location of the MIMIC3 Patient files.")
    parser.add_argument("-o", "--output_file", \
                        default='patients.shlf',
                        help="Where to store the results")
    args = parser.parse_args()
    #print args.MIMIC3_folder
    patients_shelve  = shelve.open(args.output_file)
    for d in range(1):
        file_name    = pjoin(args.MIMIC3_directory, '%02d/PATIENTS_DATA_TABLE.csv' % (d,))
        patients     = read_patients_file(file_name)
        file_name    = pjoin(args.MIMIC3_directory, '%02d/ADMISSIONS_DATA_TABLE.csv' % (d,))
        read_admissions_file(patients, file_name)
        patients_shelve.update(patients)

