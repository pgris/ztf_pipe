#!/bin/bash

python run_scripts/cadence/FakeObs.py --output_dir ../Fake_Observations
python run_scripts/cadence/metric.py --input_dir ../Fake_Observations --fileName fake_data_obs.hdf5 --outName cadenceMetric_fake_data_obs.hdf5 --nproc 1
