cd tests/package
./download_execs.ps1
cd ../..
poetry run py -m embark run tests/package/playbook.yml --report
