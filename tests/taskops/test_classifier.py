"""Tests for personal task classifier."""
import pytest
from unittest.mock import patch, MagicMock

MOCK_TAG_CONFIG = {
    "categories": {
        "project": {
            "tags": {
                "Home": "dark-blue",
                "Travel": "dark-green",
                "Health": "dark-teal",
                "Mateo": "dark-brown",
            },
        },
        "priority": {
            "tags": {
                "Priority: High": "light-red",
                "Priority: Medium": "light-orange",
                "Priority: Low": "light-warm-gray",
            },
        },
        "source": {
            "tags": {
                "Source: Manual": "light-blue",
            },
        },
        "person": {
            "default_color": "light-teal",
        },
    },
}

MOCK_CONSTANTS = {
    "workspace_gid": "ws_test",
    "aaron_gid": "aaron_test",
    "eugenia_gid": "eugenia_test",
}


@patch("execution.taskops.task_classifier.list_workspace_tags", return_value={})
@patch("execution.taskops.task_classifier.ensure_tag", return_value="tag_gid_123")
@patch("execution.taskops.task_classifier.get_asana_constants", return_value=MOCK_CONSTANTS)
@patch("execution.taskops.task_classifier._load_tag_config", return_value=MOCK_TAG_CONFIG)
class TestClassifier:
    def test_basic_classify(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Buy groceries",
            "project": "home",
            "source": "manual",
        })
        assert result["title"] == "Buy groceries"
        assert result["section"] == "To Do"
        assert result["priority"] == "medium"
        assert "Context:" in result["description"]
        assert "Project: Home" in result["description"]

    def test_description_with_context(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Call vet",
            "project": "mateo",
            "context": "Annual checkup is overdue",
            "source": "manual",
        })
        assert "Annual checkup is overdue" in result["description"]
        assert "Project: Mateo" in result["description"]

    def test_description_no_context(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Something",
            "project": "home",
            "source": "manual",
        })
        assert "Manual task" in result["description"]

    def test_priority_high(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Urgent fix",
            "project": "home",
            "priority": "high",
            "source": "manual",
        })
        assert result["priority"] == "high"

    def test_assignee_aaron(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Do taxes",
            "project": "finance",
            "assignee": "aaron",
            "source": "manual",
        })
        assert result["assignee_gid"] == "aaron_test"
        assert "Assignee: Aaron" in result["description"]

    def test_assignee_eugenia(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Call doctor",
            "project": "health",
            "assignee": "eugenia",
            "source": "manual",
        })
        assert result["assignee_gid"] == "eugenia_test"
        assert "Assignee: Eugenia" in result["description"]

    def test_assignee_none(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Shared task",
            "project": "home",
            "source": "manual",
        })
        assert result["assignee_gid"] is None

    def test_tags_include_project_priority_source(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Walk Mateo",
            "project": "mateo",
            "priority": "low",
            "source": "manual",
        })
        tag_names = [t["name"] for t in result["tags"]]
        assert "Mateo" in tag_names
        assert "Priority: Low" in tag_names
        assert "Source: Manual" in tag_names

    def test_person_tag_hints(self, mock_cfg, mock_const, mock_ensure, mock_list):
        from execution.taskops.task_classifier import classify
        result = classify({
            "title": "Schedule cleaning",
            "project": "home",
            "source": "manual",
            "tag_hints": ["Maria (Cleaner)"],
        })
        tag_names = [t["name"] for t in result["tags"]]
        assert "Maria (Cleaner)" in tag_names
