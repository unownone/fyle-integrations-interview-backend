import json

from django.urls import reverse
import pytest


@pytest.mark.django_db()
def test_get_assignments_teacher_1(api_client, teacher_1):
    response = api_client.get(
        reverse('teachers-assignments'),
        HTTP_X_Principal=teacher_1
    )

    assert response.status_code == 200

    assignments = response.json()
    assert type(assignments) == list

    for assignment in assignments:
        assert assignment['teacher'] == 1


@pytest.mark.django_db()
def test_get_assignments_teacher_2(api_client, teacher_2):
    response = api_client.get(
        reverse('teachers-assignments'),
        HTTP_X_Principal=teacher_2
    )

    assert response.status_code == 200

    assignments = response.json()
    assert type(assignments) == list

    for assignment in assignments:
        assert assignment['teacher'] == 2


@pytest.mark.django_db()
def test_invalid_grade_teacher_1(api_client, teacher_1):
    grade = 'INVALID GRADE'

    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 4,
            'grade': grade
        }),
        HTTP_X_Principal=teacher_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert 'is not a valid choice.' in error['grade'][0]


@pytest.mark.django_db()
def test_grade_draft_state_teacher_1(api_client, teacher_1):
    grade = 'A'

    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 1,
            'grade': grade
        }),
        HTTP_X_Principal=teacher_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['SUBMITTED assignments can only be graded']


@pytest.mark.django_db()
def test_grade_graded_state_teacher_1(api_client, teacher_1):
    grade = 'D'

    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 5,
            'grade': grade
        }),
        HTTP_X_Principal=teacher_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['GRADED assignments cannot be graded again']


@pytest.mark.django_db()
def test_change_of_content_teacher_1(api_client, teacher_2):
    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 2,
            'content': 'changed content',
            'grade': 'D'
        }),
        HTTP_X_Principal=teacher_2,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['Teacher cannot change the content of the assignment']


@pytest.mark.django_db()
def test_grade_invalid_state_teacher_1(api_client, teacher_1):
    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 2,
            'student': 2
        }),
        HTTP_X_Principal=teacher_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['Teacher cannot change the student who submitted the assignment']


@pytest.mark.django_db()
def test_grade_other_teacher_teacher_2(api_client, teacher_2):
    grade = 'A'
    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 4,
            'grade': grade
        }),
        HTTP_X_Principal=teacher_2,
        content_type='application/json'
    )

    assert response.status_code == 400

    error = response.json()

    assert error['non_field_errors'] == ['Teacher cannot grade for other teacher''s assignment']


@pytest.mark.django_db()
def test_grade_assignment_teacher_2(api_client, teacher_2):
    grade = 'A'
    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 3,
            'grade': grade
        }),
        HTTP_X_Principal=teacher_2,
        content_type='application/json'
    )

    assert response.status_code == 200

    assignment = response.json()

    assert assignment['content'] is not None
    assert assignment['state'] == 'GRADED'
    assert assignment['student'] == 1
    assert assignment['teacher'] == 2
    assert assignment['grade'] == grade
    assert assignment['id'] is not None


@pytest.mark.django_db()
def test_no_grade_provided(api_client, teacher_1):
    """Testing case if no input has been provided
    """
    response = api_client.patch(
        reverse('teachers-assignments'),
        data=json.dumps({
            'id': 1,
        }),
        HTTP_X_Principal=teacher_1,
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    error = response.json()
    
    assert error['non_field_errors'] == ['No Grade has been Provided']
    
@pytest.mark.django_db()
def test_no_id_provided(api_client, teacher_1):
    
    grade = 'B'
    response = api_client.patch(
        reverse('teachers-assignments'),
        data = json.dumps({
            'grade':grade
        }),
        HTTP_X_Principal = teacher_1,
        content_type = 'application/json'
    )
    
    assert response.status_code == 400
    
    error = response.json()
    
    assert error['non_field_errors'] == ['No Assignment ID Provided']
    
@pytest.mark.django_db()  
def test_wrong_id_provided(api_client, teacher_2):
    
    grade = 'A'
    response = api_client.patch(
        reverse('teachers-assignments'),
        data = json.dumps({
            'id':18, # Non Existent ID
            'grade':grade
        }),
        HTTP_X_Principal = teacher_2,
        content_type = 'application/json'
    )
    
    assert response.status_code == 400
    
    error = response.json()
    
    assert error['non_field_errors'] == ['Assignment Not Found/Access Denied']
    
    
@pytest.mark.django_db()
def test_id_as_string_provided(api_client, teacher_1):
    
    grade = 'K'
    response = api_client.patch(
        reverse('teachers-assignments'),
        data = json.dumps({
            'id':'Not a number', # Assignment ID as a number
            'grade':grade
        }),
        HTTP_X_Principal = teacher_1,
        content_type = 'application/json'
    )
    
    
    assert response.status_code == 400
    
    error = response.json()
    
    assert error['non_field_errors'] == ['Assignment ID cannot be a string']
    
@pytest.mark.django_db()
def grade_as_ASCII_equivalent_numbers(api_client, teacher_1):
        
    grade = 66
    response = api_client.patch(
        reverse('teacher-assignments'),
        data = json.dumps({
            'id':'Not a number', # Assignment ID as a number
            'grade':grade
        }),
        HTTP_X_Principal = teacher_1,
        content_type = 'application/json'
    )
    
    assert response.status_code == 400
    error = response.json()
    
    assert error['non_field_errors'] == ['Grade has to be between A and D']
    

