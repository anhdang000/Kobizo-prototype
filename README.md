# Kobizo - Real-time Transaction Analytics and Monitoring

## Overview
Kobizo is a real-time transaction analytics and monitoring system that provides fraud detection and anomaly analysis based on transaction attributes. This project includes a REST API with endpoints for predictions and feedback submission.

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine.

### Build the Docker Image
To build the Docker image, run the following command in the project directory:
```sh
docker build -t kobizo .
```

### Run the Docker Container
Run the container and map port `8080` on the host to port `5000` in the container:
```sh
docker run -p 8080:5000 kobizo
```

## API Endpoints
This API provides two main endpoints: `predict` and `feedback`. You can test them using Postman or any HTTP client.

### Predict Endpoint
**Request:**
```http
POST http://0.0.0.0:8080/predict
```

**Description:**
- This endpoint is used to make transaction fraud predictions.
- Accepts a JSON payload (TBD based on your model requirements).

**Example Response:**
```json
{
    "last_timestamp": "2024-07-30 00:02:23+00:00",
    "predictions": [
        {
            "fraud_score": 0.23147521913051605,
            "large_score": 0.5999999642372131,
            "rapid_score": 0.7685248255729675,
            "transaction_id": "0xc5061da6f7c89ab0fc20c912f058636a8c3f9d8b0456e15db30e4196d451cb60"
        },
        {
            "fraud_score": 0.23147521913051605,
            "large_score": 0.5999999642372131,
            "rapid_score": 0.7685248255729675,
            "transaction_id": "0x0232c4dd9f4b88222ed95a25f6236d7dc25b9d3dccb9a596034d37ca26807e98"
        },
        {
            "fraud_score": 0.23147521913051605,
            "large_score": 0.5999999642372131,
            "rapid_score": 0.7685248255729675,
            "transaction_id": "0xe4ecd37edb93d22eef32f62dcb397f23f75b699a0c5391e81a81f5885020e07c"
        },
        {
            "fraud_score": 0.23147521913051605,
            "large_score": 0.5999999642372131,
            "rapid_score": 0.7685248255729675,
            "transaction_id": "0x94002f1eabc5b491f9f143bd761ff693362c25e2832fce8191bbc96f5825e97e"
        },
        {
            "fraud_score": 0.23147521913051605,
            "large_score": 0.5999999642372131,
            "rapid_score": 0.7685248255729675,
            "transaction_id": "0x737bb2b517312cd2166bacb41daf5c1a80e560d3f0c8589a40791c43ec7d6566"
        }
    ]
}
```

### Feedback Endpoint
**Request:**
```http
POST http://0.0.0.0:8080/feedback
```

**Description:**
- This endpoint receives transaction feedback data for model retraining.
- Accepts a JSON array of transactions with attributes: `transaction_id`, `is_large`, `is_rapid`, and `is_fraud`.
- Feedback is then stored at PostgreSQL table `feedback_transactions`

**Example Request Body:**
```json
[
    { "transaction_id": "0xc5061da6f7c89ab", "is_large": true, "is_rapid": false, "is_fraud": false },
    { "transaction_id": "0xa17b3c59e24d8f1", "is_large": false, "is_rapid": true, "is_fraud": true }
]
```

## Postman Collection
To simplify API testing, use the provided Postman collection at `conf/rtam.postman_collection.json`
