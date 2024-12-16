# local image build
docker build -f Dockerfile.frontend -t frontend .

# local container build
docker run -p 8080:8080 frontend