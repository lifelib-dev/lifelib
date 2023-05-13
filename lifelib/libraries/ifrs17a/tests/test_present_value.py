import os.path
import pandas as pd
import pytest

thisdir = os.path.dirname(os.path.abspath(__file__))
resultdir = os.path.join(thisdir, 'expected')


def test_present_values_ep2():
    """Test present value ep.2

    Replicate the table shown at https://youtu.be/dhdA3F6ZWbs?t=448
    """
    from present_value_ep2 import ifrsvars as vars

    df = vars[(vars['EconomicBasis'] == 'L') & (vars['EstimateType'] == 'BE')].set_index(
        ['Novelty', 'AocType', 'AmountType'])['Value'].groupby(level=[0, 1, 2]).sum().unstack(level=2)

    expected = pd.read_excel(
        os.path.join(resultdir, "pv_ep2.xlsx"), index_col=[0, 1])

    pd.testing.assert_frame_equal(df, expected, check_names=False)


@pytest.mark.parametrize("reporting_node, month", [['G', 3], ['DE', 12]])
def test_present_values(reporting_node, month):
    """Test present value ep.3

    Replicate the tables for
    ReportingNode G at https://youtu.be/bhtSm0cJudo?t=115
    ReportingNode DE at https://youtu.be/bhtSm0cJudo?t=475
    """
    from present_value_ep3 import ifrsvars as vars

    filter = ((vars['EconomicBasis']=='L') & (vars['EstimateType']=='BE')
              & (vars['ReportingNode']==reporting_node) & (vars['Year']==2021) & (vars['Month']==month))

    df = vars[filter].set_index(['Novelty', 'AocType', 'AmountType'])['Value'].groupby(level=[0, 1, 2]).sum().unstack(level=2)

    expected = pd.read_excel(
        os.path.join(resultdir, "pv_ep3.xlsx"), sheet_name=reporting_node,index_col=[0, 1])

    pd.testing.assert_frame_equal(df, expected, check_names=False)

