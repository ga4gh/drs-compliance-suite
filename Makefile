DOCKER_ORG := ga4gh
DOCKER_REPO := drs-compliance-suite
# DOCKER_TAG := $(shell cat build.gradle | grep "^version" | cut -f 2 -d ' ' | sed "s/'//g")
DOCKER_TAG := test
DOCKER_IMG := ${DOCKER_ORG}/${DOCKER_REPO}:${DOCKER_TAG}

# build docker image
.PHONY: docker-build
docker-build:
	docker build -t ${DOCKER_IMG} --build-arg VERSION=${DOCKER_TAG} .

# push image to docker hub
.PHONY: docker-publish
docker-publish:
	docker image push ${DOCKER_IMG}


#dockstore workflow launch --local-entry tools/wdl/drs_compliance_suite.wdl --json tools/wdl/drs_compliance_suite.wdl.json