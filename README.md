# Export CPAD data for ADDI

* Run `make install` to install Python dependencies.
* Alter `(src|dest)_db.py` to set database connections.
* Run `make copy` to copy source database schema to destination db

## Changes

* study.name
* study_arm.description
* subject_study_arm.patient_code

Add noise to:

* patient ages (randomly add/subtract months from DOB)
* visit timing (randomly add/subtract weeks, but keep intervals consistent)
* vital sign measurements

## Author

Ken Youens-Clark <kyclark@c-path.org>
