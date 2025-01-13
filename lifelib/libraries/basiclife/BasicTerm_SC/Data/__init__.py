from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def age_at_entry():
    return model_point_table["age_at_entry"].to_numpy(dtype='int64')


def sex():
    # Not used
    return model_point_table['sex'].to_numpy()


def policy_term():
    return model_point_table['policy_term'].to_numpy(dtype='int64')


def policy_count():
    return model_point_table['policy_count'].to_numpy(dtype='float64')


def sum_assured():
    return model_point_table['sum_assured'].to_numpy(dtype='float64')


def point_id():
    return model_point_table.index.to_numpy(dtype='int64')


def mort_table_array():

    start_age = mort_table.index[0]

    return np.concatenate( 
        (np.full((start_age, len(mort_table.columns)), np.nan), mort_table.to_numpy()),
        axis=0)


def disc_rate_ann_array():
    return disc_rate_ann.to_numpy()


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("IOSpec", 1924149079376, 1924149572048)

mort_table = ("IOSpec", 1924172456224, 1924171574272)

model_point_table = ("IOSpec", 1924172272160, 1926288025184)

np = ("Module", "numpy")