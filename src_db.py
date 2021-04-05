from peewee import *
from playhouse.postgres_ext import *

database = PostgresqlDatabase('cpad')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Batch(BaseModel):
    approved_by = IntegerField(null=True)
    batch_id = AutoField()
    cdisc_version = TextField(null=True)
    connect_to = ForeignKeyField(column_name='connect_to', field='batch_id', model='self', null=True)
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    removed_on = DateTimeField(null=True)
    replaced_by = IntegerField(null=True)

    class Meta:
        table_name = 'batch'

class AlzheimerStage(BaseModel):
    alzheimer_stage_id = BigAutoField()
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    description = TextField(null=True)
    dx_criteria = TextField(null=True)
    file_version = TextField()
    name = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'alzheimer_stage'

class Arm(BaseModel):
    arm_group = TextField(null=True)
    arm_id = BigAutoField()
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    description = TextField(null=True)
    file_version = TextField()
    name = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'arm'

class Country(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    code_2l = TextField(null=True)
    code_3l = TextField(null=True, unique=True)
    country_id = BigAutoField()
    file_version = TextField()
    iso_code = IntegerField(null=True, unique=True)
    name = TextField(null=True, unique=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'country'

class TimeUnit(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    file_version = TextField()
    name = TextField(null=True, unique=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()
    time_unit_id = BigAutoField()

    class Meta:
        table_name = 'time_unit'

class Study(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    duration = IntegerField(null=True)
    file_version = TextField()
    name = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    study_id = BigAutoField()
    tier_level = IntegerField()
    time_unit = ForeignKeyField(column_name='time_unit_id', field='time_unit_id', model=TimeUnit, null=True)
    type = TextField(null=True)

    class Meta:
        table_name = 'study'

class StudyArm(BaseModel):
    arm = ForeignKeyField(column_name='arm_id', field='arm_id', model=Arm, null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    country = ForeignKeyField(column_name='country_id', field='country_id', model=Country, null=True)
    description = TextField(null=True)
    file_version = TextField()
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    study_arm_id = BigAutoField()
    study = ForeignKeyField(column_name='study_id', field='study_id', model=Study, null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'study_arm'

class Apoe(BaseModel):
    allele_one = TextField(null=True)
    allele_two = TextField(null=True)
    apoe_id = BigAutoField()
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    e4_carrier = BooleanField(null=True)
    file_version = TextField()
    genotype = TextField(null=True, unique=True)
    homozygous = BooleanField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'apoe'

class Ethnicity(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    ethnicity_id = BigAutoField()
    file_version = TextField()
    name = TextField(null=True, unique=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'ethnicity'

class Race(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    file_version = TextField()
    name = TextField(null=True, unique=True)
    project_file_id = IntegerField()
    race_id = BigAutoField()
    racial_group = TextField(null=True)
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'race'

class Subject(BaseModel):
    apoe = ForeignKeyField(column_name='apoe_id', field='apoe_id', model=Apoe, null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    education_years = IntegerField(null=True)
    ethnicity = ForeignKeyField(column_name='ethnicity_id', field='ethnicity_id', model=Ethnicity, null=True)
    family_hist_ind = BooleanField(null=True)
    file_version = TextField()
    project_file_id = IntegerField()
    race = ForeignKeyField(column_name='race_id', field='race_id', model=Race, null=True)
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    reported_ethnicity = TextField(null=True)
    reported_race = TextField(null=True)
    sex = TextField(null=True)
    subject_id = BigAutoField()
    tier_level = IntegerField()

    class Meta:
        table_name = 'subject'

class SubjectStudyArm(BaseModel):
    age = DoubleField(null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    file_version = TextField()
    patient_code = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    study_arm = ForeignKeyField(column_name='study_arm_id', field='study_arm_id', model=StudyArm, null=True)
    study_entry_offset = IntegerField(null=True)
    study_seq_num = BigIntegerField(null=True)
    subject = ForeignKeyField(column_name='subject_id', field='subject_id', model=Subject, null=True)
    subject_study_arm_id = BigAutoField()
    tier_level = IntegerField()

    class Meta:
        table_name = 'subject_study_arm'

class SubjectVisit(BaseModel):
    ad_stage = ForeignKeyField(column_name='ad_stage_id', field='alzheimer_stage_id', model=AlzheimerStage, null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    code = TextField(null=True)
    code2 = TextField(null=True)
    description = TextField(null=True)
    duration = IntegerField(null=True)
    file_version = TextField()
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    subject_study_arm = ForeignKeyField(column_name='subject_study_arm_id', field='subject_study_arm_id', model=SubjectStudyArm, null=True)
    subject_visit_id = BigAutoField()
    tier_level = IntegerField()
    time_unit = ForeignKeyField(column_name='time_unit_id', field='time_unit_id', model=TimeUnit, null=True)
    visit_offset = IntegerField(null=True)
    visit_sequence = IntegerField(null=True)
    visit_type = IntegerField(null=True)

    class Meta:
        table_name = 'subject_visit'

class AdasCog(BaseModel):
    adas_cog_id = BigAutoField()
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    commands = DecimalField(null=True)
    comprehension = DecimalField(null=True)
    concentration_distract = DecimalField(null=True)
    constructional_praxis = DecimalField(null=True)
    delay_word_recall = DecimalField(null=True)
    derived_code = TextField(null=True)
    derived_data = BinaryJSONField(null=True)
    file_version = TextField()
    ideational_praxis = DecimalField(null=True)
    maze_task = DecimalField(null=True)
    name_obj_fingers = DecimalField(null=True)
    number_cancellation = DecimalField(null=True)
    orientation = DecimalField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    remember_instructions = DecimalField(null=True)
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    score_11_item = DecimalField(null=True)
    spoken_lang_ability = DecimalField(null=True)
    subject_visit = ForeignKeyField(column_name='subject_visit_id', field='subject_visit_id', model=SubjectVisit, null=True)
    tier_level = IntegerField()
    word_find_difficulty = DecimalField(null=True)
    word_recall = DecimalField(null=True)
    word_recognition = DecimalField(null=True)

    class Meta:
        table_name = 'adas_cog'

class AlzheimerHistory(BaseModel):
    alzheimer_history_id = BigAutoField()
    alzheimer_stage = ForeignKeyField(column_name='alzheimer_stage_id', field='alzheimer_stage_id', model=AlzheimerStage, null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    diagnosis = TextField(null=True)
    diagnosis_offset = IntegerField(null=True)
    file_version = TextField()
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    subject = ForeignKeyField(column_name='subject_id', field='subject_id', model=Subject, null=True)
    subject_study_arm = ForeignKeyField(column_name='subject_study_arm_id', field='subject_study_arm_id', model=SubjectStudyArm, null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'alzheimer_history'

class Cdr(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    cdr_id = BigAutoField()
    community_affairs = DecimalField(null=True)
    derived_gs = DecimalField(null=True)
    derived_sb = DecimalField(null=True)
    file_version = TextField()
    global_score = DecimalField(null=True)
    home_hobbies = DecimalField(null=True)
    judge_prob_solving = DecimalField(null=True)
    memory = DecimalField(null=True)
    orientation = DecimalField(null=True)
    personal_care = DecimalField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    subject_visit = ForeignKeyField(column_name='subject_visit_id', field='subject_visit_id', model=SubjectVisit, null=True)
    sum_of_boxes = DecimalField(null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'cdr'

class DoseUnit(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    dose_unit_id = BigAutoField()
    file_version = TextField()
    name = TextField(null=True, unique=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'dose_unit'

class DrugClass(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    drug_class_id = BigAutoField()
    file_version = TextField()
    name = TextField(null=True, unique=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'drug_class'

class Drug(BaseModel):
    abbrev = TextField(null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    drug_class = ForeignKeyField(column_name='drug_class_id', field='drug_class_id', model=DrugClass, null=True)
    drug_id = BigAutoField()
    file_version = TextField()
    generic = TextField(null=True)
    name = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'drug'

class LabUnit(BaseModel):
    alt_name = TextField(null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    file_version = TextField()
    lab_unit_id = BigAutoField()
    name = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    tier_level = IntegerField()

    class Meta:
        table_name = 'lab_unit'

class LabTest(BaseModel):
    abbrev = TextField(null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    category = TextField(null=True)
    file_version = TextField()
    imaging_flag = BooleanField(null=True)
    lab_normal_range_f = UnknownField(null=True)  # numrange
    lab_normal_range_m = UnknownField(null=True)  # numrange
    lab_test_id = BigAutoField()
    lab_unit = ForeignKeyField(column_name='lab_unit_id', field='lab_unit_id', model=LabUnit, null=True)
    method = TextField(null=True)
    name = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    specimen = TextField(null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'lab_test'

class LabResult(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    description = TextField(null=True)
    fasting = BooleanField(null=True)
    file_version = TextField()
    lab_result_id = BigAutoField()
    lab_test = ForeignKeyField(column_name='lab_test_id', field='lab_test_id', model=LabTest, null=True)
    project_file_id = IntegerField()
    reason_not_done = TextField(null=True)
    record_num = IntegerField()
    ref_range_ind = TextField(null=True)
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    result = DecimalField(null=True)
    subject_visit = ForeignKeyField(column_name='subject_visit_id', field='subject_visit_id', model=SubjectVisit, null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'lab_result'

class Mmse(BaseModel):
    attention_and_calc = IntegerField(null=True)
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    comprehension = IntegerField(null=True)
    derived_code = TextField(null=True)
    derived_data = BinaryJSONField(null=True)
    drawing = IntegerField(null=True)
    file_version = TextField()
    mmse_id = BigAutoField()
    naming = IntegerField(null=True)
    orient_place = IntegerField(null=True)
    orient_time = IntegerField(null=True)
    project_file_id = IntegerField()
    reading = IntegerField(null=True)
    recall = IntegerField(null=True)
    record_num = IntegerField()
    registration = IntegerField(null=True)
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    repetition = IntegerField(null=True)
    subject_visit = ForeignKeyField(column_name='subject_visit_id', field='subject_visit_id', model=SubjectVisit, null=True)
    tier_level = IntegerField()
    total_score = IntegerField(null=True)
    writing = IntegerField(null=True)

    class Meta:
        table_name = 'mmse'

class ProjectFileVersion(BaseModel):
    archived_on = DateTimeField(null=True)
    check_sum = TextField()
    created_by = IntegerField()
    created_on = DateTimeField(constraints=[SQL("DEFAULT now()")])
    pipeline = TextField(null=True)
    project_file_id = IntegerField()
    size = BigIntegerField()
    version = IntegerField()

    class Meta:
        table_name = 'project_file_version'
        primary_key = False

class SubjectDisposition(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    category = TextField(null=True)
    disposition = TextField(null=True)
    disposition_offset = IntegerField(null=True)
    file_version = TextField()
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    study_phase = TextField(null=True)
    subject_disposition_id = BigAutoField()
    subject_study_arm = ForeignKeyField(column_name='subject_study_arm_id', field='subject_study_arm_id', model=SubjectStudyArm, null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'subject_disposition'

class SubjectMedication(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    dose = DecimalField(null=True)
    dose_text = TextField(null=True)
    dose_unit = ForeignKeyField(column_name='dose_unit_id', field='dose_unit_id', model=DoseUnit, null=True)
    drug = ForeignKeyField(column_name='drug_id', field='drug_id', model=Drug, null=True)
    file_version = TextField()
    indication = TextField(null=True)
    project_file_id = IntegerField()
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    reported_name = TextField(null=True)
    start_offset = IntegerField(null=True)
    stop_offset = IntegerField(null=True)
    stop_ref = TextField(null=True)
    subject = ForeignKeyField(column_name='subject_id', field='subject_id', model=Subject, null=True)
    subject_medication_id = BigAutoField()
    subject_study_arm = ForeignKeyField(column_name='subject_study_arm_id', field='subject_study_arm_id', model=SubjectStudyArm, null=True)
    tier_level = IntegerField()

    class Meta:
        table_name = 'subject_medication'

class ValidationOutput(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    domain = TextField(index=True, null=True)
    line_id = AutoField()
    message = TextField(null=True)
    record_no = IntegerField(index=True, null=True)
    rule_id = TextField(index=True, null=True)
    severity = CharField(null=True)
    validation_category = CharField(null=True)
    validation_type = CharField(null=True)
    value = TextField(null=True)
    variable = TextField(index=True, null=True)
    violation_status = CharField(null=True)

    class Meta:
        table_name = 'validation_output'

class VisitVitals(BaseModel):
    batch = ForeignKeyField(column_name='batch_id', field='batch_id', model=Batch)
    bmi = DecimalField(null=True)
    diastolic = DecimalField(null=True)
    file_version = TextField()
    height = DecimalField(null=True)
    project_file_id = IntegerField()
    pulse = DecimalField(null=True)
    record_num = IntegerField()
    removed = BooleanField(constraints=[SQL("DEFAULT false")])
    respiratory_rate = DecimalField(null=True)
    subject_visit = ForeignKeyField(column_name='subject_visit_id', field='subject_visit_id', model=SubjectVisit, null=True)
    systolic = DecimalField(null=True)
    tempurature = DecimalField(null=True)
    tier_level = IntegerField()
    visit_vitals_id = BigAutoField()
    weight = DecimalField(null=True)

    class Meta:
        table_name = 'visit_vitals'

