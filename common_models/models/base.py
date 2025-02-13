from datetime import date
from typing import Annotated

from sqlalchemy import (
    BigInteger,
    String,
    func,
    Date,
    SmallInteger,
    Integer,
    Text,
    Boolean
)
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

#  Аннотации для полей моделей

pk_bs = Annotated[int, mapped_column(BigInteger, primary_key=True, autoincrement=True)]
pk_ss = Annotated[int, mapped_column(SmallInteger, primary_key=True, autoincrement=True)]
pk_int = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

str_4000_not_null = Annotated[str, mapped_column(String(4000), nullable=False)]
str_1000_not_null = Annotated[str, mapped_column(String(1000), nullable=False)]
str_255_not_null = Annotated[str, mapped_column(String(255), nullable=False)]
str_30_not_null = Annotated[str, mapped_column(String(30), nullable=False)]
str_60_not_null = Annotated[str, mapped_column(String(60), nullable=False)]
str_16_not_null = Annotated[str, mapped_column(String(16), nullable=False)]
str_9_not_null = Annotated[str, mapped_column(String(9), nullable=False)]

str_1000 = Annotated[str, mapped_column(String(1000))]
str_255 = Annotated[str, mapped_column(String(255))]
str_100 = Annotated[str, mapped_column(String(100))]
str_60 = Annotated[str, mapped_column(String(60))]
str_13 = Annotated[str, mapped_column(String(13))]
str_9 = Annotated[str, mapped_column(String(9))]

text = Annotated[str, mapped_column(Text)]

bool_false_not_null = Annotated[bool, mapped_column(Boolean, nullable=False, default=False)]

not_null_int = Annotated[int, mapped_column(Integer, nullable=False)]
not_null_smallint = Annotated[int, mapped_column(SmallInteger, nullable=False)]
not_null_bigint = Annotated[int, mapped_column(BigInteger, nullable=False)]

create_date = Annotated[date, mapped_column(Date, nullable=False, server_default=func.current_date())]
active_from_date = Annotated[date, mapped_column(Date, nullable=False)]
active_to_date = Annotated[date, mapped_column(Date)]
