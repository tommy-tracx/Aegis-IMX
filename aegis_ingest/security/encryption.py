"""Column-level encryption utilities."""
from __future__ import annotations

import os
from typing import Iterable, Optional

from cryptography.fernet import Fernet
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BinaryType, StringType


def _build_cipher(key: Optional[bytes] = None) -> Fernet:
    """Return a :class:`Fernet` cipher, generating or loading a key."""
    raw = key or os.getenv("PII_ENCRYPTION_KEY")
    if raw is None:
        raw = Fernet.generate_key()
    elif isinstance(raw, str):
        raw = raw.encode()
    return Fernet(raw)


def encrypt_columns(df: DataFrame, columns: Iterable[str], key: Optional[bytes] = None) -> DataFrame:
    """Encrypt specified columns using Fernet symmetric encryption."""
    cipher = _build_cipher(key)
    encrypt_udf = udf(lambda x: cipher.encrypt(x.encode()) if x is not None else None, BinaryType())
    for c in columns:
        df = df.withColumn(c, encrypt_udf(col(c)))
    return df


def decrypt_columns(df: DataFrame, columns: Iterable[str], key: bytes) -> DataFrame:
    """Decrypt specified columns using the provided key."""
    cipher = _build_cipher(key)
    decrypt_udf = udf(lambda x: cipher.decrypt(x).decode() if x is not None else None, StringType())
    for c in columns:
        df = df.withColumn(c, decrypt_udf(col(c)))
    return df
