#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@c-path.org>
Date   : 2021-03-30
Purpose: Export synthetic CPAD data
"""

import argparse
import operator
import random
import src_db as src
import dest_db as dst
from typing import NamedTuple


class Args(NamedTuple):
    """ Command-line arguments """
    seed: int


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s',
                        '--seed',
                        help='Random seed',
                        metavar='int',
                        type=int,
                        default=None)

    args = parser.parse_args()

    return Args(args.seed)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    random.seed(args.seed)

    #
    # Subjects
    # Add noise to subject ids/names by shuffling
    #
    src_subjects = list(src.Subject.select())
    random.shuffle(src_subjects)

    src_subject_id_to_dst = {}
    for i, src_subject in enumerate(src_subjects, start=1):
        dst_subject = create_subject(src_subject, i)
        print(f'{i:3}: SUBJ {src_subject.subject_id} => '
              f'{dst_subject.subject_id}')
        src_subject_id_to_dst[src_subject.subject_id] = dst_subject.subject_id

    #
    # Studies/Study Arms/Subject Study Arms
    # Add noise to study ids/names by shuffling
    #
    src_studies = list(src.Study.select())
    random.shuffle(src_studies)

    for i, src_study in enumerate(src_studies, start=1):
        dst_study = create_study(src_study, i)
        print(f'{i:3}: {src_study.name} ({src_study.study_id}) => '
              f'{dst_study.name} ({dst_study.study_id})')

        arms = src.StudyArm.select().where(
            src.StudyArm.study_id == src_study.study_id)

        for j, src_study_arm in enumerate(arms, start=1):
            dst_study_arm = create_study_arm(src_study_arm, dst_study, j)
            print(f'\tARM {j}: {dst_study_arm.description}')

            subject_study_arms = src.SubjectStudyArm.select().where(
                src.SubjectStudyArm.study_arm_id == src_study_arm.study_arm_id)

            for k, src_ssa in enumerate(subject_study_arms, start=1):
                dst_subject_id = src_subject_id_to_dst[src_ssa.subject_id]
                dst_ssa = create_subject_study_arm(src_ssa, dst_subject_id,
                                                   dst_study_arm, k)
                print(f'\t\tSBJ ARM {j}: {dst_ssa.patient_code}')

                meds = src.SubjectMedication.select().where(
                    src.SubjectMedication.subject_study_arm_id ==
                    src_ssa.subject_study_arm_id)

                for src_med in meds:
                    dst_med = create_subject_medication(
                        src_med, dst_ssa, dst_subject_id)
                    print(f'\t\t\tMED {j}: {dst_med.drug.name}')

    print('Done.')


# --------------------------------------------------
def create_subject(src_subject, subject_id):
    """ Create a subject """

    dst_subject, _ = dst.Subject.get_or_create(
        subject_id=subject_id,
        race_id=src_subject.race_id,
        ethnicity_id=src_subject.ethnicity_id,
        apoe_id=src_subject.apoe_id,
        family_hist_ind=src_subject.family_hist_ind,
        education_years=src_subject.education_years,
        reported_race=src_subject.reported_race,
        reported_ethnicity=src_subject.reported_ethnicity,
        tier_level=src_subject.tier_level,
        file_version=src_subject.file_version,
        project_file_id=src_subject.project_file_id,
        removed=src_subject.removed,
        batch_id=src_subject.batch_id,
        record_num=src_subject.record_num)

    return dst_subject


# --------------------------------------------------
def create_subject_study_arm(src_ssa, dst_subject_id, dst_study_arm, count):
    """ Create a subject study arm """

    op = random.choice([operator.add, operator.sub])
    dst_ssa, _ = dst.SubjectStudyArm.get_or_create(
        subject_study_arm_id=src_ssa.subject_study_arm_id,
        study_arm_id=dst_study_arm.study_arm_id,
        subject_id=dst_subject_id,
        patient_code=f'PT {count:05}',
        study_seq_num=src_ssa.study_seq_num,
        age=op(src_ssa.age, random.randint(1, 5)),  # noise
        study_entry_offset=src_ssa.study_entry_offset,
        tier_level=src_ssa.tier_level,
        file_version=src_ssa.file_version,
        project_file_id=src_ssa.project_file_id,
        removed=src_ssa.removed,
        batch_id=src_ssa.batch_id,
        record_num=src_ssa.record_num)

    return dst_ssa


# --------------------------------------------------
def create_subject_medication(src_med, dst_ssa, dst_subject_id):
    """ Create a subject medication """

    dst_med, _ = dst.SubjectMedication.get_or_create(
        subject_medication_id=src_med.subject_medication_id,
        subject_study_arm_id=dst_ssa.subject_study_arm_id,
        subject_id=dst_subject_id,
        drug_id=src_med.drug_id,
        dose_unit_id=src_med.dose_unit_id,
        dose_text=src_med.dose_text,
        indication=src_med.indication,
        start_offset=src_med.start_offset,
        stop_offset=src_med.stop_offset,
        stop_ref=src_med.stop_ref,
        reported_name=src_med.reported_name,
        dose=src_med.dose,  # noise?
        tier_level=src_med.tier_level,
        file_version=src_med.file_version,
        project_file_id=src_med.project_file_id,
        removed=src_med.removed,
        batch_id=src_med.batch_id,
        record_num=src_med.record_num)

    return dst_med


# --------------------------------------------------
def create_study(src_study, study_id):
    """ Create a study """

    dst_study, _ = dst.Study.get_or_create(
        study_id=study_id,
        name=f'S{study_id:03d}',
        duration=src_study.duration,
        time_unit_id=src_study.time_unit_id,
        type=src_study.type,
        tier_level=src_study.tier_level,
        file_version=src_study.file_version,
        project_file_id=src_study.project_file_id,
        removed=src_study.removed,
        batch_id=src_study.batch_id,
        record_num=src_study.record_num)

    return dst_study


# --------------------------------------------------
def create_study_arm(src_study_arm, dst_study, count):
    """ Create a study_arm """

    dst_study_arm, _ = dst.StudyArm.get_or_create(
        study_arm_id=src_study_arm.study_arm_id,
        study_id=dst_study.study_id,
        batch_id=src_study_arm.batch_id,
        arm_id=src_study_arm.arm_id,
        country_id=src_study_arm.country_id,
        description=f'ARM {count:03}',
        tier_level=src_study_arm.tier_level,
        file_version=src_study_arm.file_version,
        project_file_id=src_study_arm.project_file_id,
        removed=src_study_arm.removed,
        record_num=src_study_arm.record_num)

    return dst_study_arm


# --------------------------------------------------
if __name__ == '__main__':
    main()