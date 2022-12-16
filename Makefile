DOCKER_ORG := ga4gh
DOCKER_REPO := drs-compliance-suite
DOCKER_TAG := $(shell grep 'version=' setup.py | awk -F '"' '{print $$2}')
DOCKER_IMG := ${DOCKER_ORG}/${DOCKER_REPO}:${DOCKER_TAG}

# build docker image
.PHONY: docker-build
docker-build:
	docker build -t ${DOCKER_IMG} --build-arg VERSION=${DOCKER_TAG} .

# push image to docker hub
.PHONY: docker-publish
docker-publish:
	docker image push ${DOCKER_IMG}

.PHONY: run-docker
run-docker:
	docker run -v $(PWD)/output/:/usr/src/app/output/ ga4gh/drs-compliance-suite:test \
	--server_base_url "http://host.docker.internal:8089/ga4gh/drs/v1" \
	--platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" \
	--auth_type "none" --report_path "./output/test-report.json"

# Sets the correct version for the CWL/WDL workflows, so that the correct Docker image can be pulled from the remote
.PHONY: set-workflow-versions
set-workflow-versions:
	python3 tools/set_cwl_wdl_versions.py

.PHONY: run-dockstore-wdl
run-dockstore-wdl:
	dockstore workflow launch --local-entry tools/wdl/drs_compliance_suite.wdl --json tools/wdl/drs_compliance_suite.wdl.json

.PHONY: run-cwltool-cwl
run-cwltool-cwl:
	cwltool --outdir output tools/cwl/drs_compliance_suite.cwl tools/cwl/drs_compliance_suite.cwl.json

# --script to override conflicting module versions between host computer and dockstore
.PHONY: run-dockstore-cwl
run-dockstore-cwl:
	dockstore tool launch --local-entry tools/cwl/drs_compliance_suite.cwl --json tools/cwl/drs_compliance_suite.cwl.json --script

