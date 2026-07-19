from decimal import Decimal

import pytest

from app.engineering_core.water_balance.engine import (
    WaterBalanceDomainError,
    WaterBalanceInputs,
    WaterBalanceStatus,
    calculate_water_balance,
)


VOLUME_FIELDS = (
    "external_fresh_water_m3",
    "external_reclaimed_water_m3",
    "interzone_inflow_m3",
    "wastewater_discharge_m3",
    "interzone_outflow_m3",
    "evaporation_m3",
    "product_incorporation_m3",
    "other_consumptive_use_m3",
    "opening_storage_m3",
    "closing_storage_m3",
    "internal_reuse_m3",
)


def test_balanced_case_with_storage_and_internal_reuse() -> None:
    data = WaterBalanceInputs(
        external_fresh_water_m3=Decimal("100"),
        external_reclaimed_water_m3=Decimal("20"),
        wastewater_discharge_m3=Decimal("50"),
        evaporation_m3=Decimal("30"),
        product_incorporation_m3=Decimal("10"),
        other_consumptive_use_m3=Decimal("10"),
        opening_storage_m3=Decimal("10"),
        closing_storage_m3=Decimal("30"),
        internal_reuse_m3=Decimal("40"),
        audit_tolerance_percent=Decimal("5"),
    )

    result = calculate_water_balance(data)

    assert result.total_external_inflow_m3 == Decimal("120")
    assert result.total_boundary_inflow_m3 == Decimal("120")
    assert result.total_consumptive_use_m3 == Decimal("50")
    assert result.total_boundary_outflow_m3 == Decimal("100")
    assert result.net_storage_change_m3 == Decimal("20")

    assert result.signed_balance_error_m3 == Decimal("0")
    assert result.absolute_balance_error_m3 == Decimal("0")
    assert result.balance_error_percent == Decimal("0")
    assert result.balance_closure_percent == Decimal("100")

    assert result.gross_water_demand_m3 == Decimal("160")
    assert result.internal_reuse_percent == Decimal("25")
    assert result.status == WaterBalanceStatus.BALANCED


def test_positive_error_is_unaccounted_water() -> None:
    data = WaterBalanceInputs(
        external_fresh_water_m3=Decimal("100"),
        wastewater_discharge_m3=Decimal("80"),
        audit_tolerance_percent=Decimal("5"),
    )

    result = calculate_water_balance(data)

    assert result.signed_balance_error_m3 == Decimal("20")
    assert result.unaccounted_water_m3 == Decimal("20")
    assert result.over_accounted_water_m3 == Decimal("0")
    assert result.balance_error_percent == Decimal("20")
    assert result.status == WaterBalanceStatus.IMBALANCED


def test_negative_error_is_over_accounted_water() -> None:
    data = WaterBalanceInputs(
        external_fresh_water_m3=Decimal("100"),
        wastewater_discharge_m3=Decimal("110"),
        audit_tolerance_percent=Decimal("5"),
    )

    result = calculate_water_balance(data)

    assert result.signed_balance_error_m3 == Decimal("-10")
    assert result.absolute_balance_error_m3 == Decimal("10")
    assert result.unaccounted_water_m3 == Decimal("0")
    assert result.over_accounted_water_m3 == Decimal("10")
    assert result.balance_error_percent == Decimal("10")
    assert result.balance_closure_percent == Decimal("110")
    assert result.status == WaterBalanceStatus.IMBALANCED


def test_internal_reuse_is_excluded_from_boundary_inflow() -> None:
    data = WaterBalanceInputs(
        external_fresh_water_m3=Decimal("60"),
        wastewater_discharge_m3=Decimal("60"),
        internal_reuse_m3=Decimal("40"),
    )

    result = calculate_water_balance(data)

    assert result.total_boundary_inflow_m3 == Decimal("60")
    assert result.total_boundary_outflow_m3 == Decimal("60")
    assert result.gross_water_demand_m3 == Decimal("100")
    assert result.internal_reuse_percent == Decimal("40")
    assert result.status == WaterBalanceStatus.BALANCED


@pytest.mark.parametrize(
    ("wastewater_discharge_m3", "expected_status"),
    [
        (Decimal("95"), WaterBalanceStatus.BALANCED),
        (Decimal("94.999"), WaterBalanceStatus.IMBALANCED),
    ],
)
def test_audit_tolerance_boundary(
    wastewater_discharge_m3: Decimal,
    expected_status: WaterBalanceStatus,
) -> None:
    data = WaterBalanceInputs(
        external_fresh_water_m3=Decimal("100"),
        wastewater_discharge_m3=wastewater_discharge_m3,
        audit_tolerance_percent=Decimal("5"),
    )

    result = calculate_water_balance(data)

    assert result.status == expected_status


def test_zero_activity_returns_no_flow() -> None:
    result = calculate_water_balance(WaterBalanceInputs())

    assert result.status == WaterBalanceStatus.NO_FLOW
    assert result.balance_error_percent is None
    assert result.balance_closure_percent is None
    assert result.internal_reuse_percent is None


def test_zero_inflow_with_activity_is_indeterminate() -> None:
    data = WaterBalanceInputs(
        wastewater_discharge_m3=Decimal("10"),
    )

    result = calculate_water_balance(data)

    assert result.signed_balance_error_m3 == Decimal("-10")
    assert result.balance_error_percent is None
    assert result.status == WaterBalanceStatus.INDETERMINATE


def test_storage_drawdown_with_zero_inflow_is_indeterminate() -> None:
    data = WaterBalanceInputs(
        wastewater_discharge_m3=Decimal("10"),
        opening_storage_m3=Decimal("10"),
        closing_storage_m3=Decimal("0"),
    )

    result = calculate_water_balance(data)

    assert result.signed_balance_error_m3 == Decimal("0")
    assert result.balance_error_percent is None
    assert result.status == WaterBalanceStatus.INDETERMINATE


@pytest.mark.parametrize("field_name", VOLUME_FIELDS)
def test_negative_volume_is_rejected(
    field_name: str,
) -> None:
    with pytest.raises(
        WaterBalanceDomainError,
        match="must be greater than or equal to zero",
    ):
        WaterBalanceInputs(
            **{field_name: Decimal("-0.001")}
        )


@pytest.mark.parametrize(
    "tolerance",
    [
        Decimal("-0.01"),
        Decimal("100.01"),
    ],
)
def test_invalid_audit_tolerance_is_rejected(
    tolerance: Decimal,
) -> None:
    with pytest.raises(
        WaterBalanceDomainError,
        match="must be between 0 and 100",
    ):
        WaterBalanceInputs(
            audit_tolerance_percent=tolerance
        )


@pytest.mark.parametrize(
    "value",
    [
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
    ],
)
def test_non_finite_volume_is_rejected(
    value: Decimal,
) -> None:
    with pytest.raises(
        WaterBalanceDomainError,
        match="must be finite",
    ):
        WaterBalanceInputs(
            external_fresh_water_m3=value
        )


def test_boolean_volume_is_rejected() -> None:
    with pytest.raises(
        WaterBalanceDomainError,
        match="must be a numeric value",
    ):
        WaterBalanceInputs(
            external_fresh_water_m3=True
        )


def test_invalid_decimal_string_is_rejected() -> None:
    with pytest.raises(
        WaterBalanceDomainError,
        match="must be a valid decimal value",
    ):
        WaterBalanceInputs(
            external_fresh_water_m3="not-a-number"
        )