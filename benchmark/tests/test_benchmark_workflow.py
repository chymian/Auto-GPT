import pytest
import requests

URL_BENCHMARK = "http://localhost:8080/ap/v1"
URL_AGENT = "http://localhost:8000/ap/v1"


@pytest.mark.parametrize(
    "eval_id, input_text, expected_artifact_length, test_name, should_be_successful",
    [
        (
            "81b64bf9-2b6a-4ac8-bcd2-8bfe36244ac0",
            "Write the word 'Washington' to a .txt file",
            0,
            "WriteFile",
            True,
        ),
        (
            "261ccfaa-02a2-4c1a-8a56-c76c66f7dba1",
            "Read the file called file_to_read.txt and write its content to a file called output.txt",
            1,
            "ReadFile",
            False,
        ),
    ],
)
def test_entire_workflow(
    eval_id, input_text, expected_artifact_length, test_name, should_be_successful
):
    task_request = {"eval_id": eval_id, "input": input_text}

    # First POST request
    task_response_benchmark = requests.post(
        URL_BENCHMARK + "/agent/tasks", json=task_request
    )
    assert task_response_benchmark.status_code == 200
    task_response_benchmark = task_response_benchmark.json()
    assert task_response_benchmark["input"] == input_text

    task_response_benchmark_id = task_response_benchmark["task_id"]

    response_task_agent = requests.get(
        f"{URL_AGENT}/agent/tasks/{task_response_benchmark_id}"
    )
    assert response_task_agent.status_code == 200
    response_task_agent = response_task_agent.json()
    assert len(response_task_agent["artifacts"]) == expected_artifact_length

    step_request = {"input": input_text}

    step_response = requests.post(
        URL_BENCHMARK + "/agent/tasks/" + task_response_benchmark_id + "/steps",
        json=step_request,
    )
    assert step_response.status_code == 200
    step_response = step_response.json()
    assert step_response["is_last"] == True  # Assuming is_last is always True

    step_response = requests.post(
        URL_BENCHMARK + "/agent/tasks/" + task_response_benchmark_id + "/evaluation",
        json={},
    )

    step_response = requests.post(
        URL_BENCHMARK + "/agent/tasks/" + task_response_benchmark_id + "/steps",
        json=step_request,
    )
    assert step_response.status_code == 200
    step_response = step_response.json()
    assert step_response["is_last"] == True  # Assuming is_last is always True

    eval_response = requests.post(
        URL_BENCHMARK + "/agent/tasks/" + task_response_benchmark_id + "/evaluations",
        json={},
    )
    assert eval_response.status_code == 200
    eval_response = eval_response.json()
    assert eval_response["test_name"] == test_name
    assert eval_response["metrics"]["success"] == should_be_successful
