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
```

## Run

```
python manage.py runserver
```

## Testing (CI / coverage)

```
./ci.sh
```
