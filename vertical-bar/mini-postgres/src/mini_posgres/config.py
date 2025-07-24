from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    PAGE_SIZE = 8 * 1024

