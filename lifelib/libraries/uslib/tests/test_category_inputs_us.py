"""Category names at the saved models' input boundaries."""

from contextlib import contextmanager

import modelx as mx
from modelx.core.errors import FormulaError
import pandas as pd
import pytest

from us_registry import model_path


@contextmanager
def saved_model(name):
    model = mx.read_model(model_path(name))
    try:
        yield model
    finally:
        model.close()


def set_policy_fields(projection, **changes):
    fields = dict(projection.model_point())
    fields.update(changes)
    projection.model_point[()] = pd.Series(fields, dtype=object)   # each value kept as given


@pytest.mark.parametrize(
    "model_name, field, enum_name, sentinel",
    [
        ("RILA_US_S", "crediting_type", "CreditType", "INVALID"),
        ("RILA_US_S", "iv_family", "InterimValueFamily", "INVALID"),
        ("RILA_US_S", "amort_rule", "Amortization", "INVALID"),
        ("ULSG_US_S", "premium_type", "PremiumType", "UNKNOWN"),
        ("ULSG_US_S", "premium_mode", "PremiumMode", "UNKNOWN"),
        ("UL_US_S", "db_option", "DeathBenefitOption", "OTHER"),
        ("UL_US_S", "qual_test", "Qualification", "OTHER"),
        ("UL_US_S", "premium_type", "PremiumType", "OTHER"),
        ("WholeLife_US_S", "dividend_option", "DividendOption", "OTHER"),
    ],
)
def test_policy_category_requires_a_label(model_name, field, enum_name, sentinel):
    with saved_model(model_name) as model:
        projection = model.Projection[1]
        conversion = projection.cells[field]
        enum = getattr(projection, enum_name)
        expected = enum[projection.model_point()[field]]
        assert conversion() is expected

        for value in ("unrecognized_label", sentinel, expected):
            set_policy_fields(projection, **{field: value})
            assert projection.model_point()[field] is value
            with pytest.raises(FormulaError):
                conversion()
            error = mx.get_error()
            assert isinstance(error, KeyError)
            assert error.args == (value,)


def test_nonparticipating_whole_life_dividend_label():
    with saved_model("WholeLife_US_S") as model:
        for point in (11, 12, 13):
            projection = model.Projection[point]
            assert projection.model_point()["dividend_option"] == "NONE"
            assert projection.dividend_option() is projection.DividendOption.NONE
            assert projection.div_credited(11) == 0.0


def test_dia_life_only_with_return_of_premium():
    with saved_model("DIA_US_S") as model:
        projection = model.Projection[1]
        set_policy_fields(projection, income_form="LO_ROP", db_form="ROP")
        assert projection.income_form() is projection.IncomeForm.LO_ROP
        assert projection.payout_form() is projection.IncomeForm.LO
        assert projection.db_form() is projection.DbForm.ROP

        # The model rejects unknown income-form labels when it reads the model point.
        for value in ("unrecognized_label", "INVALID", projection.IncomeForm.LO):
            set_policy_fields(projection, income_form=value)
            with pytest.raises(FormulaError):
                projection.payout_form()
            error = mx.get_error()
            assert isinstance(error, ValueError)
            assert error.args == ("invalid income_form",)


def test_spia_discount_convention_raises_at_use():
    # The Reference holds a DiscConvention member; commuted_value discounts by it and rejects any other value.
    with saved_model("SPIA_US_S") as model:
        projection = model.Projection
        enum = projection.DiscConvention
        t = 0          # policy 5 has a 120-month certain period (policy 1 has none: nothing is discounted)
        values = {}
        for member in (enum.compound, enum.simple):
            projection.commute_disc_convention = member
            values[member] = projection[5].commuted_value(t)
        assert values[enum.compound] > 0.0 and values[enum.simple] > 0.0
        assert values[enum.compound] != values[enum.simple]

        for value in ("unrecognized_label", "compound", "INVALID", 7):
            projection.commute_disc_convention = value
            with pytest.raises(FormulaError, match="invalid commute_disc_convention"):
                projection[5].commuted_value(t)


def test_myga_schedule_input_rejects_unknown_group(tmp_path):
    with saved_model("MYGA_US_S") as model:
        data = model.Data
        enum = data.Schedule
        # the schedule level holds the members' values (pandas stores IntEnum keys as integers)
        levels = data.surr_charge_table().index.get_level_values("schedule")
        groups = tuple(enum(value) for value in dict.fromkeys(levels))
        assert groups == (enum.initial, enum.renewal)

        path = tmp_path / "schedules.csv"
        path.write_text(
            "schedule,contract_year,surr_charge_rate\nunknown_schedule,1,0.09\n",
            encoding="utf-8",
        )
        data.surr_charge_file = path
        with pytest.raises(FormulaError):
            data.surr_charge_table()
        error = mx.get_error()
        assert isinstance(error, KeyError)
        assert error.args == ("unknown_schedule",)
