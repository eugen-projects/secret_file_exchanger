@echo OFF

if /I %1 == tests goto :tests
if /I %1 == coverage goto :coverage
if /I %1 == profile goto :profile
if /I %1 == clean goto :clean

goto nosuchcommand

: tests
nosetests -v --with-doctest --with-coverage --cover-html  --cover-inclusive  --cover-package=exchanger %2
goto end

: profile
nosetests --with-doctest --with-coverage --cover-html  --cover-inclusive  --cover-package=exchanger --with-profile --profile-restrict="secret_file_exchanger\\exchanger" %2
goto end

: coverage
start chrome cover/index.html
goto end

: clean
goto end

: nosuchcommand

echo 'The provided target %1 is not available'

: end