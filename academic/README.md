# SERVICE ACADEMIC MICROSERVICE
<hr>

## INSTALLATION

## clone  repository use

```bash
git clone https://github.com/Students-Projects-Docker-Automatization/sp_service_academic
```
#### Create and Activate Environment
```bash
python -m venv .venv
```
```bash
.venv\Scripts\activate
```
#### Install requirements.txt
```bash
pip install -r requirements.txt
```
## RUN SERVER
```bash
python manage.py runserver
```
# ENDPOINTS

|ACTION|METHOD|SUFIX|
|------|------|----|
|CREATE SUBJECT|POST|/sp_academic/academic/api/v1/subjects/
|LIST SUBJECT|GET|/sp_academic/academic/api/v1/subjects/
|UPDATE SUBJECT|PUT|/sp_academic/academic/api/v1/subjects/{id_subject}
|DELETE SUBJECT|DELETE|/sp_academic/academic/api/v1/subjects/{id_subject}
|CREATE SUBJECT PERIOD|POST|/sp_academic/academic/api/v1/subjectsPeriod/
|LIST SUBJECT PERIOD|GET|/sp_academic/academic/api/v1/subjectsPeriod/
|DELETE SUBJECT PERIOD|DELETE|/sp_academic/academic/api/v1/subjectsPeriod/{id_subject_period}
|GET SUBJECT PERIOD BY ID|GET|/sp_academic/academic/api/v1/subjectsPeriodDetailById/{ID SUBJECT PERIOD}
|CREATE SUBJECT STUDENT|POST|/sp_academic/academic/api/v1/subjectsStudent/
|LIST ALL SUBJECT STUDENT|GET|/sp_academic/academic/api/v1/subjectsStudent/
|DELETE SUBJECT STUDENT|DELETE|/sp_academic/academic/api/v1/subjectsStudent/{id_subject_period}
|GET SUBJECTS TEACHER|GET|/sp_academic/academic/api/v1/subjectsPeriodDetail/{id_teacher}
|GET SUBJECTS STUDENT|GET|/sp_academic/academic/api/v1/subjectStudentDetailView/{id_student}

#### CREATE SUBJECT Request and Response

##### Request body
```json
[
    {
         "name" : "FUNDAMENTOS DE PROGRAMACION",
        "code": "115101"
    },
    {
        "name" : "MATEMATICAS DISCRETAS",
        "code": "115103"
    }
]
```
##### Response body:
```json
[
    {
        "id": 6,
        "code": "115101",
        "name": "FUNDAMENTOS DE PROGRAMACION"
    },
    {
        "id": 7,
        "code": "115103",
        "name": "MATEMATICAS DISCRETAS"
    }
]
```


#### LIST SUBJECT Request and Response
##### Response body:
```json
[
    {
        "id": 1,
        "code": "1151293",
        "name": "SEMINARIO INTEGRADOR 2"
    },
    {
        "id": 2,
        "code": "1151245",
        "name": "ARQUITECTURA DE COMPUTADORES"
    }
]
```
#### UPDATE SUBJECT Request and Response

##### Request body
```json
{   
    "code": "1151293",
    "name": "SEMINARIO INTEGRADOR 5"
}
```
##### Response body:
```json
{
    "id": 8,
    "code": "1151293",
    "name": "SEMINARIO INTEGRADOR 5"
}
```

#### CREATE PERIOD SUBJECT Request and Response
##### Request body:
```json
[
    {
    "id_subject": 1151293,
    "id_teacher": 1,
    "group":"J"
    }
]
```
##### Response body:
```json
[
 {
        "id": 1,
        "year": "2022",
        "period": "2",
        "id_teacher": 1,
        "group": "C",
        "id_subject": {
            "id": 1,
            "code": "1151293",
            "name": "SEMINARIO INTEGRADOR 2"
        }
    }
]
```


#### LIST PERIOD SUBJECT Request and Response

##### Response body:
```json
[
    {
        "id": 1,
        "year": "2022",
        "period": "2",
        "id_teacher": 1,
        "group": "C",
        "id_subject": {
            "id": 1,
            "code": "1151293",
            "name": "SEMINARIO INTEGRADOR 2"
        }
    }
]
```

#### LIST SUBJECT STUDENT Request and Response

##### Request body:
```json
[
    {
        "id": 1,
        "id_student": 5,
        "id_subject_period": {
            "id": 1,
            "year": "2022",
            "period": "2",
            "id_teacher": 2,
            "group": "A",
            "id_subject": {
                "id": 1,
                "code": "1155805",
                "name": "Ingenieria de software"
            }
        }
    }
]
```
#### CREATE SUBJECT STUDENT Request and Response

##### Request body:
```json
[
    {
        "id_subject_period":1,
        "students" :[10,20]
    }
]
```

#### LIST SUBJECTS TEACHER Response

##### Response body:
```json
[
   {
        "id": 7,
        "year": "2022",
        "period": "2",
        "id_teacher": 2,
        "group": "P",
        "id_subject": {
            "id": 1,
            "code": "1151293",
            "name": "SEMINARIO INTEGRADOR 2"
        }
    }
]
```


#### LIST SUBJECTS BY STUDENT Response

##### Response body:
```json
[
    {
        "id": 1,
        "id_student": 1,
        "id_subject_period": {
            "id": 1,
            "year": "2022",
            "period": "2",
            "id_teacher": 1,
            "group": "C",
            "id_subject": {
                "id": 1,
                "code": "1151293",
                "name": "SEMINARIO INTEGRADOR 2"
            }
        }
    }
]
```

#### GET SUBJECT PERIOD BY ID

##### Response body:
```json
[
{
    "id": 1,
    "year": "2022",
    "period": "2",
    "id_teacher": 2,
    "group": "A",
    "id_subject": {
        "id": 1,
        "code": "1155805",
        "name": "Ingenieria de software"
    }
}
]
```

#### LIST STUDENTS BY SUBJECT PERIOD

/sp_academic/academic/api/v1/subjectStudentPeriod/{SUBJECT_PERIODI_ID}

##### Response body:
```json
{
    "students": [
        5,
        6,
        7
    ]
}
```
