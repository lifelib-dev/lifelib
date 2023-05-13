import os
import numpy as np
import pandas as pd
import pytest

thisdir = os.path.dirname(os.path.abspath(__file__))
resultdir = os.path.join(thisdir, 'expected')

@pytest.fixture(scope='module')
def ifrsvars():
    from template import workspace
    return workspace.database.get_ifrsvars(add_goc_attrs=True)


def test_best_estimate(ifrsvars):
    """Test best estimate table

    Replicate table shown at https://youtu.be/Qfh73qsxgNY?t=239
    """
    vars = ifrsvars
    filter = (vars['Year'] == 2021) & (vars['Month'] == 3) & (vars['EstimateType'] == 'BE')
    df = vars.loc[filter].set_index(['Novelty', 'AocType', 'EconomicBasis', 'LiabilityType']
                                    )['Value'].groupby(level=list(range(4))).sum().unstack(level=[-1, -2]).fillna(0)

    expected = pd.read_excel(os.path.join(resultdir, "template.xlsx"), sheet_name='BE', index_col=[0, 1], header=[0, 1])
    pd.testing.assert_frame_equal(df, expected)


def test_risk_adjustment(ifrsvars):
    vars = ifrsvars
    filter = (vars['Year'] == 2021) & (vars['Month'] == 3) & (vars['EstimateType'] == 'RA')
    df = vars.loc[filter].set_index(['Novelty', 'AocType', 'LiabilityType', 'EconomicBasis'])['Value'].groupby(
        level=list(range(4))).sum().unstack(level=[-1, -2]).fillna(0)

    expected = pd.read_excel(os.path.join(resultdir, "template.xlsx"), sheet_name='RA', index_col=[0, 1], header=[0, 1])
    pd.testing.assert_frame_equal(df, expected)


def test_written_actuals(ifrsvars):
    """Test written actuals

    Replicate table shown at https://youtu.be/T9bArA3QWJU?t=45
    """
    vars = ifrsvars
    filter = (vars['Year'] == 2021) & (vars['Month'] == 3) & (vars['EstimateType'] == 'A')
    df = vars.loc[filter].set_index(['AocType', 'AmountType', 'LiabilityType'])['Value'].groupby(
        level=list(range(3))).sum().unstack(level=-1).fillna(0)

    expected = pd.read_excel(os.path.join(resultdir, "template.xlsx"), sheet_name='WA', index_col=[0, 1], header=0)
    pd.testing.assert_frame_equal(df, expected, check_names=False, check_dtype=False)


def test_overdue_advanced_actuals(ifrsvars):
    """Test overdue and advanced actuals

    Replicate table shown at https://youtu.be/T9bArA3QWJU?t=75
    """
    vars = ifrsvars
    filter = (vars['Year'] == 2021) & (vars['Month'] == 3) & ((vars['EstimateType'] == 'OA') | (vars['EstimateType'] == 'AA'))
    df = vars.loc[filter].set_index(['AocType', 'EstimateType'])['Value'].groupby(
        level=list(range(2))).sum().unstack(level=-1).fillna(0)

    expected = pd.read_excel(os.path.join(resultdir, "template.xlsx"), sheet_name='AAOA', index_col=0, header=0)
    pd.testing.assert_frame_equal(df, expected, check_names=False, check_dtype=False)


def test_deferred_actuals(ifrsvars):
    """Test deferred actuals

    Replicate table shown at https://youtu.be/T9bArA3QWJU?t=92
    """
    vars = ifrsvars
    filter = (vars['Year'] == 2021) & (vars['Month'] == 3) & (vars['EstimateType'] == 'DA')
    df = vars.loc[filter].set_index(['AocType', 'EstimateType'])['Value'].groupby(
        level=list(range(2))).sum().unstack(level=-1).fillna(0)

    expected = pd.read_excel(os.path.join(resultdir, "template.xlsx"), sheet_name='DA', index_col=0, header=0)
    pd.testing.assert_frame_equal(df, expected, check_names=False, check_dtype=False)


def test_technical_margin(ifrsvars):
    """Test overdue and advanced actuals

    Replicate table shown at https://youtu.be/z4xohUbiyfM?t=85
    """
    vars = ifrsvars
    filter = (vars['Year'] == 2021) & (vars['Month'] == 3) & (
        (vars['EstimateType'] == 'C') | (vars['EstimateType'] == 'L') | (vars['EstimateType'] == 'LR'))
    df = vars.loc[filter].set_index(['Novelty', 'AocType', 'EstimateType'])['Value'].groupby(
        level=list(range(3))).sum().unstack(level=-1).fillna(0)

    expected = pd.read_excel(os.path.join(resultdir, "template.xlsx"), sheet_name='TM', index_col=[0, 1], header=0)
    pd.testing.assert_frame_equal(df, expected, check_names=False)