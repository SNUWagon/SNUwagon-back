# SNUwagon

[![Build Status](https://travis-ci.org/SNUWagon/SNUwagon-back.svg?branch=master)](https://travis-ci.org/SNUWagon/SNUwagon-back)  [![codecov](https://codecov.io/gh/SNUWagon/SNUwagon-back/branch/master/graph/badge.svg)](https://codecov.io/gh/SNUWagon/SNUwagon-back)



SNUwagon backend (frontend repository is [here](https://github.com/SNUWagon/SNUwagon-front))

## Local setting

Check you have downloaded `init_db.sh`, `set_env.sh`

```
# execute only for the first time
# if peer authenticate error occurs,
# fix pg_hba.conf (peer -> trust)
./init_db.sh

# execute on each login
source ./set_env.sh

cp pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

## Run

```
python manage.py runserver

# without authentication
NO_AUTH=True python manage.py runserver
```

## Testing
```
# syntax coverage test
./ci.sh

# API test with swagger
http://localhost:8000/swagger/
```

## Swagger Guide

We use [drf-yasg](https://github.com/axnsan12/drf-yasg/) for managing REST API.

drf-yasg uses Swagger and OpenAPI.

```python
from drf_yasg.utils import swagger_auto_schema

# add swagger decorator on each view
# See: https://github.com/axnsan12/drf-yasg/blob/master/docs/custom_spec.rst
@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def signin(request):
  ...
```
