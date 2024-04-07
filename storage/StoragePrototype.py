class StoragePrototype:
    def get_debits_by_receipt(self, receipt_id: str) -> dict:
        """
        Получение списания по указанному рецепту.

        Args:
            receipt_id (str): Идентификатор рецепта.

        Returns:
            dict: Списание по рецепту.
        """
        # Реализация метода