import sys
sys.path.append('../')
import holoclean
from detect import NullDetector, ViolationDetector
from repair.featurize import *


# 1. Setup a HoloClean session.
hc = holoclean.HoloClean(
    db_name='holo',
    domain_top_percentile=0.2,
    domain_thresh_2=0,
    weak_label_thresh=0.9,
    max_domain=10000,
    cor_strength=0.05,
    epochs=20,
    weight_decay=0,
    threads=1,
    batch_size=1,
    verbose=True,
    timeout=3*60000,
    feature_norm=True,
    weight_norm=False,
    print_fw=True
).session

# 2. Load training data and denial constraints.
hc.load_data('hospital', '../testdata/hospital.csv')
hc.load_dcs('../testdata/hospital_constraints.txt')
hc.ds.set_constraints(hc.get_dcs())

# 3. Detect erroneous cells using these two detectors.
detectors = [NullDetector(), ViolationDetector()]
hc.detect_errors(detectors)

# 4. Repair errors utilizing the defined features.
hc.setup_domain()
featurizers = [
    InitAttrFeaturizer(),
    OccurAttrFeaturizer(),
    ConstraintFeaturizer()
]

hc.repair_errors(featurizers)

# 5. Evaluate the correctness of the results.
hc.evaluate(fpath='../testdata/hospital_clean.csv',
            tid_col='tid',
            attr_col='attribute',
            val_col='correct_val')
