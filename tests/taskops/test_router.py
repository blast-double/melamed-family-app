"""Tests for personal project router."""
import pytest
from unittest.mock import patch

MOCK_CONFIG = {
    "projects": {
        "home": {
            "display_name": "Home",
            "description": "Household tasks",
            "asana_gid": "111111",
        },
        "travel": {
            "display_name": "Travel",
            "description": "Trips and bookings",
            "asana_gid": "222222",
        },
        "health": {
            "display_name": "Health",
            "description": "Medical stuff",
            "asana_gid": "333333",
        },
    },
    "fallback_project": "home",
    "asana": {
        "workspace_gid": "ws_111",
        "team_gid": "team_111",
        "aaron_gid": "aaron_111",
        "eugenia_gid": "eugenia_111",
    },
}


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear lru_cache between tests."""
    from execution.taskops import router
    router._load_config.cache_clear()
    yield
    router._load_config.cache_clear()


@patch("execution.taskops.router._load_config", return_value=MOCK_CONFIG)
class TestRouter:
    def test_get_project_gid_valid(self, mock_cfg):
        from execution.taskops.router import get_project_gid
        assert get_project_gid("travel") == "222222"

    def test_get_project_gid_fallback(self, mock_cfg):
        from execution.taskops.router import get_project_gid
        assert get_project_gid("nonexistent") == "111111"

    def test_get_project_gid_case_insensitive(self, mock_cfg):
        from execution.taskops.router import get_project_gid
        assert get_project_gid("Health") == "333333"

    def test_get_asana_constants(self, mock_cfg):
        from execution.taskops.router import get_asana_constants
        constants = get_asana_constants()
        assert constants["workspace_gid"] == "ws_111"
        assert constants["aaron_gid"] == "aaron_111"
        assert constants["eugenia_gid"] == "eugenia_111"

    def test_get_project_descriptions(self, mock_cfg):
        from execution.taskops.router import get_project_descriptions
        descs = get_project_descriptions()
        assert descs["home"] == "Household tasks"
        assert descs["travel"] == "Trips and bookings"

    def test_list_project_keys(self, mock_cfg):
        from execution.taskops.router import list_project_keys
        keys = list_project_keys()
        assert "home" in keys
        assert "travel" in keys
        assert "health" in keys
