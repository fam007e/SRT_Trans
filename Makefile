setup:
	pip install -r test_requirements.txt

test:
	export PYTHONPATH=. && pytest --cov=srt_translator --cov-report=term-missing

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-coverage:
	pytest --cov=srt_tr --cov-report=html

test-fast:
	pytest -n auto

clean:
	rm -rf reports htmlcov .pytest_cache

lint:
	pylint srt_tr.py tests
