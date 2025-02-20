from src.processing.strategies.one_hot_encoding_strategy import OneHotEncodingStrategy

class FeatureEngineeringFactory:
    """
    Fábrica para seleccionar y devolver la estrategia de Feature Engineering correspondiente.
    """

    @staticmethod
    def get_strategy(strategy_name: str):
        """
        Devuelve la estrategia de Feature Engineering basada en el nombre.

        Args:
            strategy_name (str): Nombre de la estrategia a aplicar.

        Returns:
            FeatureEngineeringStrategy: Instancia de la estrategia seleccionada.
        """
        strategies = {
            "one_hot_encoding": OneHotEncodingStrategy
        }

        if strategy_name not in strategies:
            raise ValueError(f"❌ Estrategia '{strategy_name}' no encontrada en FeatureEngineeringFactory.")

        return strategies[strategy_name]()
