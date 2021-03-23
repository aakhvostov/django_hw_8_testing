import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from students.models import Student, Course


@pytest.mark.django_db
def test_course_get(api_client, course_factory):
    """ Вывод одного курса на чтение """

    course = course_factory()
    url = reverse("courses-detail", args=(course.id,))
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    resp_json = response.json()
    assert resp_json.get("id")
    assert resp_json["id"] == course.id
    assert resp_json["name"] == course.name


@pytest.mark.django_db
def test_course_list(api_client, course_factory):
    """ Получение списка курсов """

    count_courses = 5
    course = course_factory(_quantity=count_courses)
    url = reverse("courses-list")
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    resp_json = response.json()
    assert len(resp_json) == count_courses


@pytest.mark.django_db
def test_course_name_filter_list(api_client, course_factory, student_factory):
    """ Вывод одного курса на чтение по имени """

    course_name = "test_course"
    post_url = reverse("courses-list")
    students_count = 3
    students = student_factory(_quantity=students_count)
    response_post = api_client.post(post_url, {"name": course_name, "students": [student.id for student in students]})
    assert response_post.status_code == HTTP_201_CREATED
    resp_json_post = response_post.json()
    other_courses_count = 4
    course_factory(_quantity=other_courses_count)
    url = reverse("courses-list")
    response_get = api_client.get(url, {"name": course_name})
    assert response_get.status_code == HTTP_200_OK
    resp_json_get = response_get.json()
    if len(resp_json_get) == 1:
        assert resp_json_get[0].get("id")
        assert resp_json_get[0]["id"] == resp_json_post["id"]
        assert resp_json_get[0]["name"] == course_name


@pytest.mark.django_db
def test_course_create(api_client, student_factory):
    """ Создание курса """
    course_name = "test_course"
    student = student_factory()
    post_url = reverse("courses-list")
    response_post = api_client.post(post_url, {"name": course_name, "students": student.id})
    assert response_post.status_code == HTTP_201_CREATED
    resp_json_post = response_post.json()
    assert resp_json_post.get("id")
    assert resp_json_post["name"] == course_name


@pytest.mark.django_db
def test_course_patch(api_client, course_factory, student_factory):
    """ Обновление курса """
    course = course_factory()
    patch_url = reverse("courses-detail", args=(course.id,))
    new_course_name = "new_course_name"
    response_patch = api_client.patch(patch_url, {"name": new_course_name})
    assert response_patch.status_code == HTTP_200_OK
    resp_json_patch = response_patch.json()
    assert resp_json_patch.get("id")
    assert resp_json_patch["name"] == new_course_name


@pytest.mark.django_db
def test_course_delete(api_client, course_factory, student_factory):
    """ Удаление курса """
    course = course_factory()
    delete_url = reverse("courses-detail", args=(course.id,))
    response_delete = api_client.delete(delete_url)
    assert response_delete.status_code == HTTP_204_NO_CONTENT
