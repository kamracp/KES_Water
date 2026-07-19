from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Final


ZERO: Final = Decimal("0")
HUNDRED: Final = Decimal("100")


class WaterBalanceDomainError(ValueError):
    """Raised when water-balance data violates domain rules."""


class WaterBalanceStatus(StrEnum):
    BALANCED = "BALANCED"
    IMBALANCED = "IMBALANCED"
    NO_FLOW = "NO_FLOW"
    INDETERMINATE = "INDETERMINATE"


VOLUME_FIELD_NAMES: Final[tuple[str, ...]] = (
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


def _to_decimal(
    value: Decimal | int | float | str,
    field_name: str,
) -> Decimal:
    if isinstance(value, bool):
        raise WaterBalanceDomainError(
            f"{field_name} must be a numeric value."
        )

    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise WaterBalanceDomainError(
            f"{field_name} must be a valid decimal value."
        ) from exc

    if not decimal_value.is_finite():
        raise WaterBalanceDomainError(
            f"{field_name} must be finite."
        )

    return decimal_value


@dataclass(frozen=True, slots=True)
class WaterBalanceInputs:
    """
    Water volumes measured over one consistent audit period.

    Internal reuse is tracked as a circularity KPI and is not counted
    as a new boundary inflow.
    """

    external_fresh_water_m3: Decimal = ZERO
    external_reclaimed_water_m3: Decimal = ZERO
    interzone_inflow_m3: Decimal = ZERO

    wastewater_discharge_m3: Decimal = ZERO
    interzone_outflow_m3: Decimal = ZERO
    evaporation_m3: Decimal = ZERO
    product_incorporation_m3: Decimal = ZERO
    other_consumptive_use_m3: Decimal = ZERO

    opening_storage_m3: Decimal = ZERO
    closing_storage_m3: Decimal = ZERO

    internal_reuse_m3: Decimal = ZERO
    audit_tolerance_percent: Decimal = Decimal("5")

    def __post_init__(self) -> None:
        for field_name in VOLUME_FIELD_NAMES:
            decimal_value = _to_decimal(
                getattr(self, field_name),
                field_name,
            )

            if decimal_value < ZERO:
                raise WaterBalanceDomainError(
                    f"{field_name} must be greater than or equal to zero."
                )

            object.__setattr__(
                self,
                field_name,
                decimal_value,
            )

        tolerance = _to_decimal(
            self.audit_tolerance_percent,
            "audit_tolerance_percent",
        )

        if tolerance < ZERO or tolerance > HUNDRED:
            raise WaterBalanceDomainError(
                "audit_tolerance_percent must be between 0 and 100."
            )

        object.__setattr__(
            self,
            "audit_tolerance_percent",
            tolerance,
        )


@dataclass(frozen=True, slots=True)
class WaterBalanceResult:
    total_external_inflow_m3: Decimal
    total_boundary_inflow_m3: Decimal
    total_consumptive_use_m3: Decimal
    total_boundary_outflow_m3: Decimal
    net_storage_change_m3: Decimal

    signed_balance_error_m3: Decimal
    absolute_balance_error_m3: Decimal
    balance_error_percent: Decimal | None
    balance_closure_percent: Decimal | None

    unaccounted_water_m3: Decimal
    over_accounted_water_m3: Decimal

    gross_water_demand_m3: Decimal
    internal_reuse_percent: Decimal | None

    audit_tolerance_percent: Decimal
    status: WaterBalanceStatus


def calculate_water_balance(
    data: WaterBalanceInputs,
) -> WaterBalanceResult:
    """
    Calculate a boundary-aware water balance.

    Signed balance error:
        boundary inflow - boundary outflow - net storage change

    A positive error represents unaccounted water.
    A negative error represents over-accounted water.
    """

    total_external_inflow = (
        data.external_fresh_water_m3
        + data.external_reclaimed_water_m3
    )

    total_boundary_inflow = (
        total_external_inflow
        + data.interzone_inflow_m3
    )

    total_consumptive_use = (
        data.evaporation_m3
        + data.product_incorporation_m3
        + data.other_consumptive_use_m3
    )

    total_boundary_outflow = (
        data.wastewater_discharge_m3
        + data.interzone_outflow_m3
        + total_consumptive_use
    )

    net_storage_change = (
        data.closing_storage_m3
        - data.opening_storage_m3
    )

    signed_balance_error = (
        total_boundary_inflow
        - total_boundary_outflow
        - net_storage_change
    )

    absolute_balance_error = abs(signed_balance_error)

    accounted_volume = (
        total_boundary_outflow
        + net_storage_change
    )

    if total_boundary_inflow > ZERO:
        balance_error_percent = (
            absolute_balance_error
            / total_boundary_inflow
            * HUNDRED
        )

        balance_closure_percent = (
            accounted_volume
            / total_boundary_inflow
            * HUNDRED
        )

        status = (
            WaterBalanceStatus.BALANCED
            if balance_error_percent
            <= data.audit_tolerance_percent
            else WaterBalanceStatus.IMBALANCED
        )
    else:
        balance_error_percent = None
        balance_closure_percent = None

        has_activity = (
            total_boundary_outflow != ZERO
            or net_storage_change != ZERO
            or data.internal_reuse_m3 != ZERO
        )

        status = (
            WaterBalanceStatus.INDETERMINATE
            if has_activity
            else WaterBalanceStatus.NO_FLOW
        )

    unaccounted_water = max(
        signed_balance_error,
        ZERO,
    )

    over_accounted_water = max(
        -signed_balance_error,
        ZERO,
    )

    gross_water_demand = (
        total_boundary_inflow
        + data.internal_reuse_m3
    )

    internal_reuse_percent = (
        data.internal_reuse_m3
        / gross_water_demand
        * HUNDRED
        if gross_water_demand > ZERO
        else None
    )

    return WaterBalanceResult(
        total_external_inflow_m3=total_external_inflow,
        total_boundary_inflow_m3=total_boundary_inflow,
        total_consumptive_use_m3=total_consumptive_use,
        total_boundary_outflow_m3=total_boundary_outflow,
        net_storage_change_m3=net_storage_change,
        signed_balance_error_m3=signed_balance_error,
        absolute_balance_error_m3=absolute_balance_error,
        balance_error_percent=balance_error_percent,
        balance_closure_percent=balance_closure_percent,
        unaccounted_water_m3=unaccounted_water,
        over_accounted_water_m3=over_accounted_water,
        gross_water_demand_m3=gross_water_demand,
        internal_reuse_percent=internal_reuse_percent,
        audit_tolerance_percent=data.audit_tolerance_percent,
        status=status,
    )