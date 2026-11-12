from app.domain.entities import InventoryItem
from app.domain.inventory_cost import apply_stock_receipt
from app.schemas.admin_resources import InventoryCreate, InventoryUpdate


class InventoryService:
    """Inventory use cases including weighted average cost."""

    def __init__(self, repository) -> None:
        """
        @param repository: Inventory repository
        @return: None
        """
        self._repository = repository

    def list_items(self) -> list[InventoryItem]:
        """
        @return: Inventory rows
        """
        return self._repository.list()

    def get_item(self, item_id: str) -> InventoryItem | None:
        """
        @param item_id: Inventory id
        @return: Inventory item or None
        """
        return self._repository.get_by_id(item_id)

    def create_item(self, payload: InventoryCreate) -> InventoryItem:
        """
        @param payload: Create DTO
        @return: Created inventory item
        """
        data = payload.model_dump()
        return self._repository.create(InventoryItem(**data))

    def update_item(self, item_id: str, payload: InventoryUpdate) -> InventoryItem:
        """
        @param item_id: Inventory id
        @param payload: Update DTO (supports optional stock receipt)
        @return: Updated inventory item
        """
        current = self._repository.get_by_id(item_id)
        if not current:
            raise KeyError(item_id)

        changes = payload.model_dump(exclude_unset=True)
        incoming_qty = changes.pop("incoming_quantity", None)
        unit_cost = changes.pop("unit_cost", None)

        if incoming_qty:
            next_qty, next_avg = apply_stock_receipt(
                current.quantity,
                current.average_cost,
                int(incoming_qty),
                float(unit_cost or 0),
            )
            changes["quantity"] = next_qty
            changes["average_cost"] = next_avg

        return self._repository.update(item_id, **changes)

    def delete_item(self, item_id: str) -> None:
        """
        @param item_id: Inventory id
        @return: None
        """
        self._repository.delete(item_id)
