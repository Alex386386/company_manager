from typing import Annotated

from pydantic import Field

validate_str_9 = Annotated[str, Field(min_length=1, max_length=9)]
validate_str_13 = Annotated[str, Field(min_length=1, max_length=13)]
validate_str_16 = Annotated[str, Field(min_length=1, max_length=16)]
validate_str_30 = Annotated[str, Field(min_length=1, max_length=30)]
validate_str_60 = Annotated[str, Field(min_length=1, max_length=60)]
validate_str_100 = Annotated[str, Field(min_length=1, max_length=100)]
validate_str_255 = Annotated[str, Field(min_length=1, max_length=255)]
validate_str_1000 = Annotated[str, Field(min_length=1, max_length=1000)]
validate_small_int = Annotated[int, Field(ge=0, le=32767)]
