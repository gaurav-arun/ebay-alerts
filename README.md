# eBay Alerts

A Full Stack Web Application that allows a user to configure alerts for specific search phrases on eBay. The application then sends periodic updates with related products to the user via email. Additionally, the user receives periodic emails with insights about the variation in prices of the products in the last 2 weeks.

## Project Setup

To run this project, you will need to configure the following: 
- `eBay app credentials` to fetch accurate search results from the eBay marketplace.
- `SMTP credentials` for receiving emails in your mailbox. 

The following section shows how to edit the `docker-compose.yml` file directly to run the project locally. If you prefer not to edit the `docker-compose.yml`, you can configure these variables in the `.env.docker` file in the `alerts_backend` and `analytics_backend` directories respectively.

- Override these `environment` variables for the `alerts_celery` service:
```environment
- EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
- EMAIL_HOST_USER=<smtp-username>
- EMAIL_HOST_PASSWORD=<smtp-password>
- EMAIL_PORT=<smtp-port>

- EBAY_API_ENV=production
- EBAY_CLIENT_ID_PRODUCTION=<your-eBay-production-app-client-id>
- EBAY_CLIENT_SECRET_PRODUCTION=<eBay-production-app-client-secret>
```

- Override these `environment` variables for the `analytics_celery` service:
```environment
- EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
- EMAIL_HOST_USER=<your-smtp-username>
- EMAIL_HOST_PASSWORD=<your-smtp-password>
- EMAIL_PORT=2525
```

- Run the project using the docker-compose:
```command
$ docker-compose up
```

- Finally, Configure a few alerts from the [Alerts Dashboard](http://localhost:3000) and you should start receiving product price alerts and insights in your mailbox. The product insights are generated at 30-minute intervals by default. 

## Architecture

![image](https://github.com/gaurav-arun/ebay_alerts/assets/12862099/edf9e8c3-c375-4e6c-a5de-a4b7120ffcf4)

At a high level, this project comprises 4 different systems:
1. Alerts Service
2. Analytics Service
3. PubSub Service
4. Third-Party Services - eBay and SMTP(Email)

### Alerts Service

Alerts Service follows a microservice architecture with the following components:
1. `Alerts Frontend`
   - Configure and manage alerts by the end-user
2. `Alerts API Server`
   - Exposes REST endpoints for the Alerts Frontend
   - Offloads blocking/time-consuming tasks to the background workers
   - Publishes the changes in the alert configuration to the PubSub channel. This information is used to track user activity and to tweak product insights accordingly.
3. `Alerts Backgroud Workers`
   - Fetches product information from eBay
   - Sends out periodic alerts to the user via email
   - Publishes the product information to the PubSub channel
5. `Alerts DB`
   - OLTP Database optimized for servicing API requests from the Alerts Frontend

### Analytics Service

Analytics Service also follows microservices architecture with the following components:
1. `Analytics Consumer Service`
   - Subscribes to specific topics on the PubSub channels
   - Consumes events received on this channel
   - Offloads the processing of these events to the background workers
3. `Analytics Background Workers`
   - Processes consumed events and stores the data in OLAP-optimized schema
   - Performs analytics on the data and generates product insights
   - Sends product insights to the end-user
5. `Analytics DB`
   - OLAP Database

### PubSub Service

`PubSub` is a shared resource between Alerts Service and Analytics Service. Alerts Service publishes events on PubSub channels. Analytics Service subscribes to these channels and consumes events that arrive on this channel in order.

### Third-Party Services

1. `eBay API Server` provides REST endpoints used by Alerts Service to fetch product information based on search phrases.
2. `SMTP Server` sends out email notifications to the users.

## Project Structure

```
├── README.md
├── alerts_backend
│   ├── alerts_backend
│   │   ├── celery.py
│   ├── alerts
│   │   ├── tasks.py
├── alerts_frontend
├── analytics
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
- `alerts_frontend`: React application for Alerts Frontend
- `analytics`: Django application for Analytics Background Workers
- `analytics/insights/management/commands/pubsub_event_consumer.py`: Management command to run Analytics Consumer Service
- `ebay_mock`: Mocks service for Ebay API. To run this set `EBAY_API_ENV=mock`. It mimics the price variation of eBay products and returns a random list of products in the response.
- `pubsub`: A thin wrapper around Redis PubSub API. This module is used by Alerts Service as well as Analytics Service. It defines a standard interface for the PubSub events and standard implementation for initializing a `Producer` and a `Consumer` instance. 

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
  - For OLAP, I choose PostgreSQL primarily for the ease of setup, the scale of the project, and my familiarity with the technology. There are other options like Apache Cassandra or Hadoop that may be a better choice if we are dealing with a massive scale and require complex analytical processing and decision-making based on historical or aggregated data.
- PubSub
  - I needed asynchronous messaging, typically a publisher-subscriber model, to provide a way for `Alerts Service` and `Analytics Service` to communicate in a decoupled manner. While there are other options like Apache Kafka that support streaming, total ordering, etc. at a massive scale, for this project, Redis Pub/Sub seemed capable enough to do the job. It is also easier to set up.
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

## Possible Imporvements

## References
- CSS files for frontend [app](https://github.com/taniarascia/primitive)
