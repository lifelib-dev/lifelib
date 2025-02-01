"""
The :mod:`~basiclife.BasicTerm_SC.Data` space is for reading
input data from internal files, and provides the data
to :mod:`~basiclife.BasicTerm_SC.Projection` in the form
of numpy arrays. Below is the list the references
for input data and associated files in this space.

.. list-table:: Input Fiels and References
   :header-rows: 1

   * - Reference
     - Input File
   * - :attr:`model_point_table`
     - *model_point_table.xlsx*
   * - :attr:`mort_table`
     - *mort_table.xlsx*
   * - :attr:`disc_rate_ann`
     - *disc_rate_ann.xlsx*

.. rubric:: Parameters and References

(In all the sample code below,
the global variable `BasicTerm_SC` refers to the
:mod:`~basiclife.BasicTerm_SC` model.)

Attributes:

    model_point_table: This reference holds model point data
        as a pandas DataFrame read from
        the internal associated file, *model_point_table.xlsx*.

        .. code-block::

            >>> BasicTerm_SC.Data.model_poit_table
                       age_at_entry sex  policy_term  policy_count  sum_assured
            point_id
            1                    47   M           10             1       622000
            2                    29   M           20             1       752000
            3                    51   F           10             1       799000
            4                    32   F           20             1       422000
            5                    28   M           15             1       605000
                            ...  ..          ...           ...          ...
            9996                 47   M           20             1       827000
            9997                 30   M           15             1       826000
            9998                 45   F           20             1       783000
            9999                 39   M           20             1       302000
            10000                22   F           15             1       576000

            [10000 rows x 5 columns]

        The columns of the DataFrame represents model point attributes,
        such as ``age_at_entry``, ``sex``, ``policy_term``,
        ``policy_count`` and ``sum_assured``.
        The columns are then referenced from the cells with the same names.
        Each of the cells then returns its attribute for all model points
        as a numpy array.
        Unlike :mod:`~basiclife.BasicTerm_S`, ``point_id`` is not used
        as the model point identifier. Instead, the array index is used.

        .. seealso::

           * :func:`age_at_entry`
           * :func:`sex`
           * :func:`policy_term`
           * :func:`sum_assured`


    disc_rate_ann: This refernce holds annual discount rates
        by duration as a pandas Series read from
        the internal associated file, *model_point_table.xlsx*.

        .. code-block::

            >>> BasicTerm_SC.Data.disc_rate_ann
            year
            0      0.00000
            1      0.00555
            2      0.00684
            3      0.00788
            4      0.00866

            146    0.03025
            147    0.03033
            148    0.03041
            149    0.03049
            150    0.03056
            Name: disc_rate_ann, Length: 151, dtype: float64

        This is referenced from :func:`disc_rate_ann_array`,
        which converts the Series into a numpy array, and is
        referenced from the :mod:`~basiclife.BasicTerm_SC.Projection` space.

        .. seealso::

           * :func:`disc_rate_ann_array`

    mort_table: This reference holds a mortality table
        by age and duration as a DataFrame.
        The table is read from the associated internal file, *mort_table.xlsx*.

        .. code-block::

            >>> BasicTerm_SC.Data.mort_table
                        0         1         2         3         4         5
            Age
            18   0.000231  0.000254  0.000280  0.000308  0.000338  0.000372
            19   0.000235  0.000259  0.000285  0.000313  0.000345  0.000379
            20   0.000240  0.000264  0.000290  0.000319  0.000351  0.000386
            21   0.000245  0.000269  0.000296  0.000326  0.000359  0.000394
            22   0.000250  0.000275  0.000303  0.000333  0.000367  0.000403
            ..        ...       ...       ...       ...       ...       ...
            116  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            117  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            118  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            119  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            120  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000

            [103 rows x 6 columns]

        This is referenced from :func:`mort_table_array`,
        which converts the DataFrame into a numpy array.
        :func:`mort_table_array` adds rows filled with ``nan`` to
        align the row index with age.
        :func:`mort_table_array` is referenced from
        the :mod:`~basiclife.BasicTerm_SC.Projection` space.

        .. seealso::

           * :func:`mort_table_array`

    np: The `numpy`_ module.
    pd: The `pandas`_ module.

.. _numpy:
   https://numpy.org/

.. _pandas:
   https://pandas.pydata.org/

.. _new_pandas:
   https://docs.modelx.io/en/latest/reference/space/generated/modelx.core.space.UserSpace.new_pandas.html

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def age_at_entry():
    """Age at entry

    Returns the age at entry attribute of all model points
    as a numpy array of type *int64*.
    """
    return model_point_table["age_at_entry"].to_numpy(dtype='int64')


def sex():
    """Sex

    Returns the age at entry attribute of all model points
    as a numpy array. This is not used by default.
    """
    # Not used
    return model_point_table['sex'].to_numpy()


def policy_term():
    """Policy term

    Returns the policy term attribute of all model points
    as a numpy array of type *int64*.
    """
    return model_point_table['policy_term'].to_numpy(dtype='int64')


def policy_count():
    """Policy counts

    Returns the policy count attribute of all model points
    as a numpy array of type *float64*.
    """
    return model_point_table['policy_count'].to_numpy(dtype='float64')


def sum_assured():
    """Sum assured

    Returns the sum assured attribute of all model points
    as a numpy array of type *float64*.
    """
    return model_point_table['sum_assured'].to_numpy(dtype='float64')


def point_id():
    """Point ID

    Returns the point id attribute of all model points
    as a numpy array of type *int64*.
    This attribute is not used, and the index of the numpy array is
    used as the model point identifier.
    """
    return model_point_table.index.to_numpy(dtype='int64')


def mort_table_array():
    """Mortality table as a numpy array

    This cells reference :attr:`mort_table`, and
    returns a numpy array holding mortality rates by age and duration.
    Rows filled with the ``nan`` values are inserted to
    make the row index integers align with the age at entry.
    """
    start_age = mort_table.index[0]

    return np.concatenate( 
        (np.full((start_age, len(mort_table.columns)), np.nan), mort_table.to_numpy()),
        axis=0)


def disc_rate_ann_array():
    """Annual discount rates

    This cells reference :attr:`disc_rate_ann`, and
    returns a numpy array holding annual discount rates by duration.
    """
    return disc_rate_ann.to_numpy()


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("IOSpec", 1924149079376, 1924149572048)

mort_table = ("IOSpec", 1924172456224, 1924171574272)

model_point_table = ("IOSpec", 1924172272160, 1926288025184)

np = ("Module", "numpy")