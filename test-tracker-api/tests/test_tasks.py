def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover the API",
            "status": "InProgress",
            "priority": "High",
            "assignee": "Ada",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover the API"
    assert body["status"] == "InProgress"
    assert body["priority"] == "High"
    assert body["assignee"] == "Ada"
    assert "id" in body


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Bad priority", "priority": "VeryHigh"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Unknown field", "made_up": "value"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "first task"})

    response = client.get("/tasks?status=Done")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "high task", "priority": "High"})
    client.post("/tasks", json={"title": "low task", "priority": "Low"})

    response = client.get("/tasks?priority=High")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "high task"
    assert payload[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]
    assert response.json()["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id does-not-exist not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(f"/tasks/{created_task['id']}", json={"title": "patched title"})

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "patched title"
    assert body["description"] == ""
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/does-not-exist", json={"title": "patched title"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id does-not-exist not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": "Done"})

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to Done" in response.json()["detail"]


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": "ToDo"})

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to ToDo" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id does-not-exist not found"
