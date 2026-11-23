import pytest
from src.views_greeting import get_mask_account, greeting_home

@pytest.mark.parametrize("data", "expect", [
    ("2020-01-10 10:23:22", ["Доброе Утро"]),
    (),
]
                         )