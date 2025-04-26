IMAGE_NAME=wikipedia-agent
GCP_PROJECT=genibuilder
AR_REGISTRY_NAME=wikipedia-agent
AR_REGION=asia-east1
VERSION=latest
IMAGE_URI=${AR_REGION}-docker.pkg.dev/${GCP_PROJECT}/${AR_REGISTRY_NAME}/${IMAGE_NAME}:${VERSION}

build:
	docker build -t "${IMAGE_NAME}" .
	
build-m1:
	docker build --platform linux/amd64 -t "${IMAGE_NAME}" .

docker-auth:
	gcloud auth configure-docker ${AR_REGION}-docker.pkg.dev

tag:
	docker tag "${IMAGE_NAME}" "${IMAGE_URI}"

push:
	docker push "${IMAGE_URI}"

deploy: docker-auth build-m1 tag push
	@echo "Image successfully built and pushed to: ${IMAGE_URI}"

verify:
	gcloud artifacts docker images describe "${IMAGE_URI}"