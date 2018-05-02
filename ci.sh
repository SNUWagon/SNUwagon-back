set -ev
echo "\n*** VALIDATING SCRIPTS\n"
flake8 --config ./flake8
echo "\n\033[42mSUCCESSED VALIDATING SCRIPTS\033[0m"

echo "\n *** TESTING COVERAGE\n"
coverage run --branch --source "./api" manage.py test
