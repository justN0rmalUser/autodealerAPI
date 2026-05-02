"""
Firebird Database Wrapper Library.

Надежная и атомарная обертка над драйвером fdb для работы с БД.
"""

# -----------------------------------------------------------------------------
# 1. МЕТАДАННЫЕ ПАКЕТА
# -----------------------------------------------------------------------------
# Версию лучше хранить здесь или в pyproject.toml. Для явности оставим здесь.
__version__ = "0.1.2"
# -----------------------------------------------------------------------------
# 2. ИМПОРТ ПУБЛИЧНОГО API
# -----------------------------------------------------------------------------
# Мы импортируем только то, что должно быть доступно пользователю сразу.
# Это реализует принцип "Четкой структуры" — пользователь не лазает по подмодулям.

try:
    from .core.connection.connect import Connection
    from .core.connection.transactions import Transaction
    from .config import DatabaseConfig
    from .exceptions.config_exceptions import IncompleteConfigurationError
    from .types.models import AcceptedTables
    from .types.builder import Build
    from .types.schemas.product_schema import Product
except ImportError as e:
    # Принцип "Надежность": если библиотека сломана при импорте, мы должны об этом знать четко.
    # Но не скрываем ошибку, а пробрасываем её с контекстом.
    raise ImportError(f"Failed to initialize library components: {e}") from e

# -----------------------------------------------------------------------------
# 3. ЯВНЫЙ СПИСОК ЭКСПОРТА (__all__)
# -----------------------------------------------------------------------------
# Принцип "Атомарность и Четкость": явно указываем, что доступно при
# импорте через 'from package import *' это предотвращает засорение неймспейса.

__all__ = [
    "__version__",
    "Connection",
    "Transaction",
    "DatabaseConfig",
    "AcceptedTables",
    "Build",
    "Product",
    "IncompleteConfigurationError"
]
