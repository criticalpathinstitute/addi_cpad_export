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
                print(f'\t\tSBJ ARM: {dst_ssa.patient_code}')

                az_histories = src.AlzheimerHistory.select().where(
                    src.AlzheimerHistory.subject_study_arm_id ==
                    src_ssa.subject_study_arm_id)

                for src_az_hist in az_histories:
                    dst_az_hist = create_alzheimer_history(
                        src_az_hist, dst_ssa, dst_subject_id)
                    print(f'\t\t\tAZHIST: {dst_az_hist.diagnosis}')

                dispositions = src.SubjectDisposition.select().where(
                    src.SubjectDisposition.subject_study_arm_id ==
                    src_ssa.subject_study_arm_id)

                for src_disp in dispositions:
                    dst_disp = create_subject_disposition(src_disp, dst_ssa)
                    print(f'\t\t\tDISP: {dst_disp.disposition}')

                meds = src.SubjectMedication.select().where(
                    src.SubjectMedication.subject_study_arm_id ==
                    src_ssa.subject_study_arm_id)

                for src_med in meds:
                    dst_med = create_subject_medication(
                        src_med, dst_ssa, dst_subject_id)
                    print(f'\t\t\tMED: {dst_med.drug.name}')

                visits = src.SubjectVisit.select().where(
                    src.SubjectVisit.subject_study_arm_id ==
                    src_ssa.subject_study_arm_id)

                for src_visit in visits:
                    dst_visit = create_subject_visit(src_visit, dst_ssa)
                    print(f'\t\t\tVISIT: {dst_visit.code}')

                    adas_cogs = src.AdasCog.select().where(
                        src.AdasCog.subject_visit_id ==
                        src_visit.subject_visit_id)

                    for src_adas_cog in adas_cogs:
                        dst_adas_cog = create_adas_cog(src_adas_cog, dst_visit)
                        print(f'\t\t\t\tADAS COG: '
                              f'{dst_adas_cog.adas_cog_id}')

                    cdrs = src.Cdr.select().where(
                        src.Cdr.subject_visit_id == src_visit.subject_visit_id)

                    for src_cdr in cdrs:
                        dst_cdr = create_cdr(src_cdr, dst_visit)
                        print(f'\t\t\t\tCDR: ' f'{dst_cdr.cdr_id}')

                    vitals = src.VisitVitals.select().where(
                        src.VisitVitals.subject_visit_id ==
                        src_visit.subject_visit_id)

                    for src_vital in vitals:
                        dst_vital = create_visit_vital(src_vital, dst_visit)
                        print(f'\t\t\t\tVITALS: '
                              f'{dst_vital.visit_vitals_id}')

                    mmse = src.Mmse.select().where(src.Mmse.subject_visit_id ==
                                                   src_visit.subject_visit_id)

                    for src_mmse in mmse:
                        dst_mmse = create_mmse(src_mmse, dst_visit)
                        print(f'\t\t\t\tMMSE: ' f'{dst_mmse.mmse_id}')

                    lab_results = src.LabResult.select().where(
                        src.LabResult.subject_visit_id ==
                        src_visit.subject_visit_id)

                    for src_lab_result in lab_results:
                        dst_lab = create_lab_result(src_lab_result, dst_visit)
                        print(f'\t\t\t\tLAB: ' f'{dst_lab.result}')

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
def create_alzheimer_history(src_az_hist, dst_ssa, dst_subject_id):
    """ Create alzheimer history """

    dst_az_hist, _ = dst.AlzheimerHistory.get_or_create(
        alzheimer_history_id=src_az_hist.alzheimer_history_id,
        subject_study_arm_id=dst_ssa.subject_study_arm_id,
        alzheimer_stage_id=src_az_hist.alzheimer_stage_id,
        subject_id=dst_subject_id,
        diagnosis=src_az_hist.diagnosis,
        diagnosis_offset=src_az_hist.diagnosis_offset,
        tier_level=src_az_hist.tier_level,
        file_version=src_az_hist.file_version,
        project_file_id=src_az_hist.project_file_id,
        removed=src_az_hist.removed,
        batch_id=src_az_hist.batch_id,
        record_num=src_az_hist.record_num)

    return dst_az_hist


# --------------------------------------------------
def create_subject_disposition(src_disp, dst_ssa):
    """ Create a subject disposition """

    dst_disp, _ = dst.SubjectDisposition.get_or_create(
        subject_disposition_id=src_disp.subject_disposition_id,
        subject_study_arm_id=dst_ssa.subject_study_arm_id,
        category=src_disp.category,
        disposition=src_disp.disposition,
        study_phase=src_disp.study_phase,
        tier_level=src_disp.tier_level,
        file_version=src_disp.file_version,
        project_file_id=src_disp.project_file_id,
        removed=src_disp.removed,
        batch_id=src_disp.batch_id,
        record_num=src_disp.record_num)

    return dst_disp


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
def create_subject_visit(src_visit, dst_ssa):
    """ Create a subject visit """

    dst_visit, _ = dst.SubjectVisit.get_or_create(
        subject_visit_id=src_visit.subject_visit_id,
        subject_study_arm_id=dst_ssa.subject_study_arm_id,
        ad_stage_id=src_visit.ad_stage_id,
        visit_offset=src_visit.visit_offset,
        code=src_visit.code,
        code2=src_visit.code2,
        description=src_visit.description,
        duration=src_visit.duration,  # noise?
        time_unit_id=src_visit.time_unit_id,
        visit_type=src_visit.visit_type,
        visit_sequence=src_visit.visit_sequence,
        tier_level=src_visit.tier_level,
        file_version=src_visit.file_version,
        project_file_id=src_visit.project_file_id,
        removed=src_visit.removed,
        batch_id=src_visit.batch_id,
        record_num=src_visit.record_num)

    return dst_visit


# --------------------------------------------------
def create_adas_cog(src_adas_cog, dst_visit):
    """ Create adas_cog """

    dst_adas_cog, _ = dst.AdasCog.get_or_create(
        adas_cog_id=src_adas_cog.adas_cog_id,
        subject_visit_id=dst_visit.subject_visit_id,
        word_recall=src_adas_cog.word_recall,
        commands=src_adas_cog.commands,
        constructional_praxis=src_adas_cog.constructional_praxis,
        delay_word_recall=src_adas_cog.delay_word_recall,
        name_obj_fingers=src_adas_cog.name_obj_fingers,
        ideational_praxis=src_adas_cog.ideational_praxis,
        orientation=src_adas_cog.orientation,
        word_recognition=src_adas_cog.word_recognition,
        remember_instructions=src_adas_cog.remember_instructions,
        spoken_lang_ability=src_adas_cog.spoken_lang_ability,
        word_find_difficulty=src_adas_cog.word_find_difficulty,
        comprehension=src_adas_cog.comprehension,
        maze_task=src_adas_cog.maze_task,
        number_cancellation=src_adas_cog.number_cancellation,
        concentration_distract=src_adas_cog.concentration_distract,
        score_11_item=src_adas_cog.score_11_item,
        derived_code=src_adas_cog.derived_code,
        derived_data=src_adas_cog.derived_data,
        tier_level=src_adas_cog.tier_level,
        file_version=src_adas_cog.file_version,
        project_file_id=src_adas_cog.project_file_id,
        removed=src_adas_cog.removed,
        batch_id=src_adas_cog.batch_id,
        record_num=src_adas_cog.record_num)

    return dst_adas_cog


# --------------------------------------------------
def create_cdr(src_cdr, dst_visit):
    """ Create cdr """

    dst_cdr, _ = dst.Cdr.get_or_create(
        cdr_id=src_cdr.cdr_id,
        subject_visit_id=dst_visit.subject_visit_id,
        memory=src_cdr.memory,
        orientation=src_cdr.orientation,
        judge_prob_solving=src_cdr.judge_prob_solving,
        community_affairs=src_cdr.community_affairs,
        home_hobbies=src_cdr.home_hobbies,
        personal_care=src_cdr.personal_care,
        global_score=src_cdr.global_score,
        derived_gs=src_cdr.derived_gs,
        sum_of_boxes=src_cdr.sum_of_boxes,
        derived_sb=src_cdr.derived_sb,
        tier_level=src_cdr.tier_level,
        file_version=src_cdr.file_version,
        project_file_id=src_cdr.project_file_id,
        removed=src_cdr.removed,
        batch_id=src_cdr.batch_id,
        record_num=src_cdr.record_num)

    return dst_cdr


# --------------------------------------------------
def create_visit_vital(src_vital, dst_visit):
    """ Create a visit vital """

    dst_vital, _ = dst.VisitVitals.get_or_create(
        visit_vitals_id=src_vital.visit_vitals_id,
        subject_visit_id=dst_visit.subject_visit_id,
        height=src_vital.height,
        weight=src_vital.weight,
        bmi=src_vital.bmi,
        tempurature=src_vital.tempurature,  # typo in schema, tempura -- yum!
        pulse=src_vital.pulse,
        respiratory_rate=src_vital.respiratory_rate,
        systolic=src_vital.systolic,
        diastolic=src_vital.diastolic,
        tier_level=src_vital.tier_level,
        file_version=src_vital.file_version,
        project_file_id=src_vital.project_file_id,
        removed=src_vital.removed,
        batch_id=src_vital.batch_id,
        record_num=src_vital.record_num)

    return dst_vital


# --------------------------------------------------
def create_mmse(src_mmse, dst_visit):
    """ Create MMSE """

    dst_mmse, _ = dst.Mmse.get_or_create(
        mmse_id=src_mmse.mmse_id,
        subject_visit_id=dst_visit.subject_visit_id,
        orient_time=src_mmse.orient_time,
        orient_place=src_mmse.orient_place,
        registration=src_mmse.registration,
        attention_and_calc=src_mmse.attention_and_calc,
        recall=src_mmse.recall,
        naming=src_mmse.naming,
        repetition=src_mmse.repetition,
        reading=src_mmse.reading,
        writing=src_mmse.writing,
        drawing=src_mmse.drawing,
        total_score=src_mmse.total_score,
        derived_code=src_mmse.derived_code,
        derived_data=src_mmse.derived_data,
        tier_level=src_mmse.tier_level,
        file_version=src_mmse.file_version,
        project_file_id=src_mmse.project_file_id,
        removed=src_mmse.removed,
        batch_id=src_mmse.batch_id,
        record_num=src_mmse.record_num)

    return dst_mmse


# --------------------------------------------------
def create_lab_result(src_lab_result, dst_visit):
    """ Create Lab Result """

    dst_lab_result, _ = dst.LabResult.get_or_create(
        lab_result_id=src_lab_result.lab_result_id,
        subject_visit_id=dst_visit.subject_visit_id,
        lab_test_id=src_lab_result.lab_test_id,
        result=src_lab_result.result,
        description=src_lab_result.description,
        ref_range_ind=src_lab_result.ref_range_ind,
        reason_not_done=src_lab_result.reason_not_done,
        fasting=src_lab_result.fasting,
        tier_level=src_lab_result.tier_level,
        file_version=src_lab_result.file_version,
        project_file_id=src_lab_result.project_file_id,
        removed=src_lab_result.removed,
        batch_id=src_lab_result.batch_id,
        record_num=src_lab_result.record_num)

    return dst_lab_result


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
