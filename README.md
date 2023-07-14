# eBay Alerts

A Fullstack Web Application that allows a user to configure alerts for specific search phrases on eBay. The application then sends periodic updates with related products to the user via email. Additionally, the user receives periodic emails with insights about the variation in prices of the products in the last 2 weeks.

## Features
- Phase 1
  | Feature | Status|
  |---------|-------|
  |Create all CRUD operations |✔️|
  |Add a simple UI (preferred in ReactJs) to create new alerts  |✔️|
  |The solution should work locally using: docker-compose up |✔️|
  |Expose the documentation of the API with swagger |✔️|
  |Provide a short explanation for your architecture and design decisions |✔️|
  |Provide documentation about project setup, run tests, and run the solution locally |✔️|
  |Add tests whenever possible|✖️|
  
- Phase 2
  | Feature | Status|
  |---------|-------|
  |Collect data about user alerts and product prices|✔️|
  |Generate useful product insights|✔️|
  |Send periodic emails to the user with product insights|✔️|
  |Use a shared resource for the Phase 1 application to communicate with the Phase 2 application|✔️| 
  |Add tests whenever possible.|✖️|
  
## Project Setup
- Clone this repository
  ```
  git clone https://github.com/gaurav-arun/ebay_alerts.git
  ```
- Navigate to the root directory of the project.

- Override the `environment` variables for the `alerts_celery` service and the `analytics_celery` service in the `docker-compose.yml`. `docker-compose.yml` is available in the root directory of the project.

  > While copy-pasting credentials from eBay or Mailtrap to `docker-compose.yml`, don't forget to remove quotes around them.
  
   ### alerts_celery
   ```environment
   - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   - EMAIL_HOST_USER=<smtp-username>
   - EMAIL_HOST_PASSWORD=<smtp-password>
   - EMAIL_PORT=<smtp-port>
   
   - EBAY_API_ENV=production
   - EBAY_CLIENT_ID_PRODUCTION=<your-eBay-production-app-client-id>
   - EBAY_CLIENT_SECRET_PRODUCTION=<eBay-production-app-client-secret>
   ```
   
   ### analytics_celery
   ```environment
   - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   - EMAIL_HOST_USER=<smtp-username>
   - EMAIL_HOST_PASSWORD=<smtp-password>
   - EMAIL_PORT=<smtp-port>
   ```

- Run the project using the docker-compose:
```command
$ docker-compose up
```

- Once all containers are up, head to the [Alerts Dashboard](http://localhost:3000) and configure a few alerts. You should start receiving product price alerts and insights in the configured mailbox. The product insights are generated at 30-minute intervals by default.
- Swagger UI can be opened [here](http://localhost:8080).

## Architecture
![ebay_alerts_architecture](https://github.com/gaurav-arun/ebay-alerts/assets/12862099/3a288dab-494b-47f3-bb3e-f05631f8e83a)



At a high level, this project comprises 4 different systems:
1. Alerts Service
2. Analytics Service
3. PubSub Service
4. Third-Party Services - eBay and SMTP(Email)

### Alerts Service

Alerts Service follows a microservice architecture with the following components:
1. `Alerts Frontend`
   - To configure and manage alerts by the end-user
2. `Alerts API Server`
   - Exposes REST endpoints for the Alerts Frontend
   - Offloads blocking/time-consuming tasks to the background workers
   - Publishes the changes in the alert configuration to the PubSub channel
3. `Alerts Backgroud Workers`
   - Fetches product information from eBay
   - Sends out periodic alerts to the user via email
   - Publishes the product information to the PubSub channel
5. `Alerts DB`
   - OLTP Database optimized for servicing API requests from the Alerts Frontend

### Analytics Service

Analytics Service also follows microservices architecture with the following components:
1. `Analytics Consumer Service`
   - Subscribes to specific topics on the PubSub channel
   - Consumes events received on this channel
   - Offloads the processing of these events to the background workers
3. `Analytics Background Workers`
   - Processes consumed events and stores the data in OLAP-optimized schema
   - Performs analytics on the data and generates product insights
   - Sends product insights to the end-user
5. `Analytics DB`
   - OLAP Database

### PubSub Service

`PubSub` is a shared resource between Alerts Service and Analytics Service. `Alerts Service` publishes events on PubSub channels. `Analytics Service` subscribes to these channels and consumes events that arrive on this channel in order. This information received over the `PubSub` channel is used by `Analytics Service` to track alert configuration and product prices.

### Third-Party Services

1. `eBay API Server` provides REST endpoints that `Alerts Service` uses to fetch product information based on search phrases.
2. `SMTP Server` sends out email notifications to the users.


## Project Structure
⚠️ The visualization below only shows the directories and files that are relevant to understand the overall structure of the project.
```
├── README.md
├── alerts_backend
│   ├── .env.docker
│   ├── alerts_backend
│   │   ├── celery.py
│   ├── alerts
│   │   ├── tasks.py
│   ├── ebay_sdk
├── alerts_frontend
├── analytics
│   ├── .env.docker
│   ├── analytics
│   │   ├── celery.py
│   ├── insights
│   │   ├── tasks.py
│   │   ├── management
│   │   │   └── commands
│   │   │       └── pubsub_event_consumer.py
├── docker-compose.yml
├── ebay_mock
└── pubsub
```

- `alerts_backend`: Django application for Alerts API Service and Alerts Background Workers
- `alerts_backend/ebay_sdk`: Provides easy-to-use utility methods for fetching product information from eBay for specified search phrases. It abstracts away all the complexities like:
  - Acquiring an authorization token using client credentials grant flow
  - Caching and reusing the authorization token until it expires
  - Reacquiring an authorization token when it expires
- `alerts_frontend`: React application for Alerts Frontend
- `analytics`: Django application for Analytics Background Workers
- `analytics/insights/management/commands/pubsub_event_consumer.py`: Management command to run Analytics Consumer Service
- `ebay_mock`: Mocks service for Ebay API. To run this set environment variable `EBAY_API_ENV=mock` under the `alerts_celery` service in the `docker-compose.yml`. It mimics the price variation of eBay products and returns a random list of products in the response. It is useful for local development or if you don't have eBay app credentials handy.
- `pubsub`: A thin wrapper around Redis PubSub API. This module is used by `Alerts Service` as well as `Analytics Service`. It defines a standard interface for the PubSub events and concrete implementations for creating a `RedisProducer` and a  `RedisConsumer` instance. 

## Technologies Used

| Service  | Technologies/Tools|
|----------|----------|
| Alerts Frontend   | React JS |
| Alerts API Service   | Django  |
| Alerts Background Workers   | Celery + Redis Broker  |
| Alerts DB  | PostgreSQL  |
| PubSub     | Redis Pub/Sub |
| Analytics Consumer Service | Django |
| Analytics Background Workers | Celery + Redis Broker |
| Analytics DB | PostgresSQL |
| SMTP Service | Mailtrap |

## API Documentation

OpenAPI 3 documentation for `Alerts API Service` is automatically generated using [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) and hosted using [Swagger UI](https://hub.docker.com/r/swaggerapi/swagger-ui) on [http://localhost:8080](http://localhost:8080)

## Design Considerations

- Background Workers
  - Celery support multiple brokers like Rabbit MQ, Kafka, etc. However, I chose Redis because I also needed a caching layer to store the eBay Auth Token acquired using the [Client Credentials Grant Flow](https://developer.ebay.com/api-docs/static/oauth-client-credentials-grant.html) required for eBay [search API](https://developer.ebay.com/api-docs/buy/browse/resources/item_summary/methods/search#uri.filter). 
- Database
  - For OLTP, I needed a relational database. PostgreSQL is one of the popular choices for this.
  - For OLAP, I choose PostgreSQL primarily for the ease of setup, the scale of the project, and my familiarity with the technology. Other options like Apache Cassandra or Hadoop may be a better choice if we are dealing with a massive scale and require complex analytical processing and decision-making based on historical or aggregated data.
- PubSub
  - I needed asynchronous messaging, typically a publisher-subscriber model, to provide a way for `Alerts Service` and `Analytics Service` to communicate in a decoupled manner. While other options like Apache Kafka support streaming, total ordering, etc. at a massive scale, for this project, Redis Pub/Sub seemed capable enough to do the job. It is also easier to set up.
- Consumer Service
  - Conceptually, it is a dedicated service that consumes events from the `PubSub` channels and persists them in DB for further processing. For this project, I am running the `Consumer Service` as a separate process within the `Analytics Background Worker` service itself. It is implemented as follows:
  - I have created a new management command called `pubsub_event_consumer` under the `insights` app. In the `analytics/dockerfiles/celery.dockerfile` this management command is started as a separate process using docker's CMD directive.
    ```dockerfile
    CMD celery -A analytics beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & \
        celery -A analytics worker --loglevel=info & \
        python manage.py pubsub_event_consumer
    ```
- SMTP Service
  - I choose a free and easy-to-configure solution - [Mailtrap](https://mailtrap.io/). It is also possible to setup local SMTP service using docker images like [inbucket](https://hub.docker.com/r/inbucket/inbucket/) or [Mailhog](https://hub.docker.com/r/mailhog/mailhog/). However, I felt that the HTML rendering capabilities of these solutions are very limited. I also like the HTML Check and Span Analysis features provided by `Mailtrap`.

- `ebay_sdk`: I evaluated the publicly available [ebaysdk](https://github.com/timotheus/ebaysdk-python), but the interface and configuration were not easy to understand. Moreover, it relies on eBay's SOAP APIs and seems pretty outdated. So I decided to implement my version of `ebay_sdk` using eBay's REST APIs and only the required parts.

## Assumptions
- The product alert frequency of [2, 10, 30] minutes does not change often. If not, this list should be populated using an API call to the Alerts Backend.
- By extension, celery crontabs are hard-coded to run at [2, 10, 30] minutes.
- Same for product insight frequency. Currently, it is hard-coded in celery crontab to run every 30 minutes.

## Possible Improvements
#### Tooling
- Use `Poetry` for dependency management. Currently, it's a single `requirements.txt` file with both the development and production dependencies.
- `Pytest` can be used for writing unit tests and generating code coverage.
- `pubsub` and `ebay_sdk` can be maintained as separate git repositories and then added as a submodule of the main git repository. Another option is to publish these modules as PIP installable packages and then use `Poetry` to pin these modules as dependencies.
- `Dockerfile` and `docker-compose.yml` are not production ready because they expose non-standard ports and use bind mounts.
- We should use `-slim`, or `-alpine` versions of the images if possible to reduce the build time and image sizes.
#### Code
- [Must Have] Unit test for all the modules
- `alerts_backend.alerts.task.send_alert`: Improved error handling for Alert tasks and possibly split the tasks into smaller subtasks - e.g. `fetch_product_info()`, `send_product_alert()`, `publish_product_info()`. The results of each of these steps can be persisted in DB. That way each of these steps can happen in isolation and can be retried on failure.
- `analytics.insights.task.send_product_insight`: It stores insights generated for each alert in memory. A better approach would be to persist the generated insights in DB and then use a separate task to send out emails with retries on failure.
- Add type hints and docstrings wherever possible.
## References
- CSS files for frontend [app](https://github.com/taniarascia/primitive)
