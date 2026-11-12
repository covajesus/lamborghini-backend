"""Weighted average cost helpers for inventory receipts."""


def apply_stock_receipt(
    current_qty: int,
    current_avg: float,
    incoming_qty: int,
    unit_cost: float,
) -> tuple[int, float]:
    """
    Apply a stock receipt using weighted average cost.

    @param current_qty: Current on-hand quantity
    @param current_avg: Current average unit cost
    @param incoming_qty: Units received
    @param unit_cost: Unit cost of the receipt
    @return: Tuple of (new quantity, new average cost)
    """
    qty = max(0, int(current_qty or 0))
    avg = float(current_avg or 0)
    incoming = int(incoming_qty or 0)
    cost = float(unit_cost or 0)

    if incoming < 0:
        raise ValueError("Incoming quantity cannot be negative")
    if incoming == 0:
        return qty, avg
    if cost < 0:
        raise ValueError("Unit cost cannot be negative")

    next_qty = qty + incoming
    if qty <= 0:
        return next_qty, round(cost, 2)

    next_avg = ((qty * avg) + (incoming * cost)) / next_qty
    return next_qty, round(next_avg, 2)
