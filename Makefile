.PHONY: validate_conditions

validate:
	python -m scripts.validate_conditions

run:
	docker-compose up -d --build
