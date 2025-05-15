- GitHub Repository
  https://github.com/uuboyscy/taxi_trip_pipeline

- Data source
  https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

- Create network
    ```shell
    docker network create \
        --driver=bridge \
        --subnet=172.28.0.0/16 \
        --ip-range=172.28.5.0/24 \
        --gateway=172.28.5.254 \
        taxi-demo
    ```

- Build airflow
    ```shell
    docker run -it -d \
    --name airflow-server \
    --network=taxi-demo \
    -p 8080:8080 \
    -v $(PWD)/dags:/opt/airflow/dags \
    -v $(PWD)/logs:/opt/airflow/logs \
    -v $(PWD)/utils:/opt/airflow/utils \
    -v $(PWD)/tasks:/opt/airflow/tasks \
    -v $(PWD)/test:/opt/airflow/test \
    -e PYTHONPATH=/opt/airflow \
    -e API_HOST=http://host.docker.internal:5432 \
    --ip 172.28.5.11 \
    apache/airflow:latest airflow standalone
    ```

    - Get into airflow container to create a user to login web UI easily
        ```shell
        docker exec -it airflow-server /bin/bash

        # Execute following command in container
        airflow users create \
            --username airflow \
            --firstname airflow \
            --password airflow \
            --lastname airflow \
            --role Admin \
            --email your_email@example.com
        ```

- Build postgres
    ```shell
    docker run --network=taxi-demo --name taxi-trip-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mypassword --ip 172.28.5.12 -d postgres
    ```

- Build dbt
    - cd to dbt folder and then `poetry install`
    - dbt debug to test connection
