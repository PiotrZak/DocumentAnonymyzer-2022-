docker login hack4lawregistry.azurecr.io

docker tag hack4law_api hack4lawregistry.azurecr.io/hack4law_api
docker push hack4lawregistry.azurecr.io/hack4law_api

docker tag hack4law_frontend hack4lawregistry.azurecr.io/hack4law_frontend
docker push hack4lawregistry.azurecr.io/hack4law_frontend