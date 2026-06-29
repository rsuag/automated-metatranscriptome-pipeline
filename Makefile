SHELL := /bin/bash

.PHONY: validate plan radar run-qc run-functional run-expression summarize all

validate:
	python3 scripts/validate_inputs.py --project config/project.yaml

plan: validate
	python3 scripts/plan_routes.py --project config/project.yaml

radar:
	python3 scripts/method_radar.py --sources config/method_sources.json --project config/project.yaml

run-qc: validate
	bash bin/run_pipeline.sh qc

run-functional: validate
	bash bin/run_pipeline.sh functional

run-expression: validate
	bash bin/run_pipeline.sh expression

summarize:
	python3 scripts/summarize_outputs.py --project config/project.yaml

all: validate plan radar run-qc run-functional run-expression summarize

