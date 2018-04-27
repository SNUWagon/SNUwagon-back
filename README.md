# SNUwagon

[![Build Status](https://travis-ci.org/SNUWagon/SNUwagon-back.svg?branch=master)](https://travis-ci.org/SNUWagon/SNUwagon-back) [![Coverage Status](https://coveralls.io/repos/github/SNUWagon/SNUwagon-back/badge.svg?branch=master)](https://coveralls.io/github/SNUWagon/SNUwagon-back?branch=master)

SNUwagon backend

## Local setting

Check you have downloaded `.coveralls.yml`, `init_db.sh`, `set_env.sh`

```
# execute only for the first time
# if peer authenticate error occurs,
# fix pg_hba.conf (peer -> trust)
./init_db.sh

# execute on each login
source ./set_env.sh
```

## Run

```
python manage.py runserver
```

## Testing (CI / coverage)

```
./ci.sh
```
