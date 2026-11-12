from app.domain.inventory_cost import apply_stock_receipt


def test_first_receipt_sets_average_cost() -> None:
    qty, avg = apply_stock_receipt(0, 0, 10, 1000)
    assert qty == 10
    assert avg == 1000


def test_weighted_average_cost() -> None:
    qty, avg = apply_stock_receipt(10, 1000, 10, 2000)
    assert qty == 20
    assert avg == 1500


def test_empty_receipt_keeps_values() -> None:
    qty, avg = apply_stock_receipt(5, 900, 0, 1200)
    assert qty == 5
    assert avg == 900
