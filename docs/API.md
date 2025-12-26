# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, no authentication required. In production, implement JWT tokens.

---

## Violation Detection Endpoints

### 1. Detect Violations from Image

**POST** `/violations/detect`

Analyze an image for traffic violations.

**Request:**

```bash
curl -X POST "http://localhost:8000/api/violations/detect" \
  -F "file=@image.jpg" \
  -F "latitude=28.7041" \
  -F "longitude=77.1025" \
  -F "location_name=NH-48 Toll" \
  -F "camera_id=CAM-001"
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | Image file (JPG/PNG) |
| latitude | float | Yes | Location latitude |
| longitude | float | Yes | Location longitude |
| location_name | string | Yes | Human-readable location |
| camera_id | string | No | Camera identifier |

**Response:**

```json
{
  "status": "success",
  "violations_detected": 2,
  "details": {
    "helmet_detections": 3,
    "plate_detections": 2,
    "violations": [
      {
        "type": "HELMET_NOT_WORN",
        "bbox": [100, 150, 200, 250],
        "confidence": 0.95,
        "severity": "HIGH",
        "penalty": 500,
        "vehicle_number": "DL-01AB1234"
      }
    ]
  }
}
```

---

### 2. List Violations

**GET** `/violations/list`

Retrieve list of recorded violations.

**Request:**

```bash
curl "http://localhost:8000/api/violations/list?skip=0&limit=100&vehicle_number=DL-01AB1234"
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| skip | integer | 0 | Number of records to skip |
| limit | integer | 100 | Maximum records to return |
| vehicle_number | string | null | Filter by vehicle number |

**Response:**

```json
{
  "status": "success",
  "total": 150,
  "violations": [
    {
      "id": 1,
      "violation_type": "HELMET_NOT_WORN",
      "vehicle_number": "DL-01AB1234",
      "timestamp": "2024-01-15T10:30:00",
      "location": "NH-48 Toll",
      "severity": "HIGH"
    }
  ]
}
```

---

### 3. Get Violation Details

**GET** `/violations/{violation_id}`

Get specific violation details.

**Request:**

```bash
curl "http://localhost:8000/api/violations/1"
```

**Response:**

```json
{
  "status": "success",
  "violation": {
    "id": 1,
    "violation_type": "HELMET_NOT_WORN",
    "severity": "HIGH",
    "vehicle_number": "DL-01AB1234",
    "timestamp": "2024-01-15T10:30:00",
    "location": "NH-48 Toll",
    "latitude": 28.7041,
    "longitude": 77.1025,
    "image_path": "/data/evidence/violation_1.jpg",
    "detection_confidence": 0.95
  }
}
```

---

## E-Challan Endpoints

### 1. Issue E-Challan

**POST** `/challan/issue`

Create and issue E-challan for a violation.

**Request:**

```bash
curl -X POST "http://localhost:8000/api/challan/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "violation_id": 1,
    "owner_name": "John Doe",
    "owner_phone": "+919876543210",
    "owner_email": "john@example.com",
    "registration_number": "DL-01AB1234",
    "evidence_image_url": "https://example.com/evidence.jpg"
  }'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| violation_id | integer | Yes | ID of the violation |
| owner_name | string | Yes | Vehicle owner name |
| owner_phone | string | Yes | Owner phone number |
| owner_email | string | Yes | Owner email |
| registration_number | string | Yes | Vehicle registration |
| evidence_image_url | string | No | Evidence image URL |

**Response:**

```json
{
  "status": "success",
  "message": "Challan issued successfully",
  "challan": {
    "id": 1,
    "challan_number": "ECH-20240115-12345",
    "status": "ISSUED",
    "violation_type": "HELMET_NOT_WORN",
    "vehicle_number": "DL-01AB1234",
    "owner_name": "John Doe",
    "penalty_amount": 500,
    "payment_deadline": "2024-01-30T23:59:59",
    "issued_date": "2024-01-15T10:30:00"
  }
}
```

---

### 2. Get Challan Details

**GET** `/challan/{challan_id}`

Retrieve challan information.

**Request:**

```bash
curl "http://localhost:8000/api/challan/1"
```

**Response:**

```json
{
  "status": "success",
  "challan": {
    "challan_number": "ECH-20240115-12345",
    "status": "ISSUED",
    "violation_type": "HELMET_NOT_WORN",
    "violation_date": "2024-01-15T10:30:00",
    "location": "NH-48 Toll",
    "vehicle_number": "DL-01AB1234",
    "owner_name": "John Doe",
    "penalty_amount": 500,
    "paid_amount": 0,
    "balance_amount": 500,
    "payment_deadline": "2024-01-30T23:59:59"
  }
}
```

---

### 3. Record Payment

**POST** `/challan/{challan_id}/payment`

Record payment for challan.

**Request:**

```bash
curl -X POST "http://localhost:8000/api/challan/1/payment" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500,
    "payment_method": "ONLINE",
    "transaction_id": "TXN-123456789"
  }'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| amount | float | Yes | Payment amount |
| payment_method | string | Yes | ONLINE, OFFLINE, etc. |
| transaction_id | string | No | Transaction reference |

**Response:**

```json
{
  "status": "success",
  "message": "Payment recorded successfully",
  "challan_status": "PAID"
}
```

---

## Analytics Endpoints

### 1. Get Heatmap Data

**GET** `/analytics/heatmap/data`

Get violation distribution for heatmap visualization.

**Request:**

```bash
curl "http://localhost:8000/api/analytics/heatmap/data?days=7&violation_type=HELMET_NOT_WORN"
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| days | integer | 7 | Number of days to analyze |
| violation_type | string | null | Filter by type |
| min_lat, max_lat | float | null | Latitude bounds |
| min_lng, max_lng | float | null | Longitude bounds |

**Response:**

```json
{
  "status": "success",
  "heatmap_data": [
    {
      "latitude": 28.7041,
      "longitude": 77.1025,
      "violation_count": 15,
      "violation_type": "HELMET_NOT_WORN",
      "severity_score": 8.5
    }
  ],
  "total_violations": 150,
  "period": "Last 7 days"
}
```

---

### 2. Get Summary Statistics

**GET** `/analytics/summary`

Get overall statistics.

**Request:**

```bash
curl "http://localhost:8000/api/analytics/summary?days=30"
```

**Response:**

```json
{
  "status": "success",
  "period": "Last 30 days",
  "summary": {
    "total_violations": 1250,
    "total_challans_issued": 980,
    "total_revenue_collected": 490000,
    "violations_by_type": {
      "HELMET_NOT_WORN": 625,
      "TRIPLE_RIDING": 375,
      "SIGNAL_VIOLATION": 200,
      "SPEED_VIOLATION": 50
    },
    "violations_by_location": {
      "NH-48 Toll": 245,
      "Ring Road": 189
    }
  }
}
```

---

### 3. Get High-Risk Zones

**GET** `/analytics/high-risk-zones`

Get locations with highest violation density.

**Request:**

```bash
curl "http://localhost:8000/api/analytics/high-risk-zones?days=30&limit=10"
```

**Response:**

```json
{
  "status": "success",
  "period": "Last 30 days",
  "high_risk_zones": [
    {
      "location": "NH-48 Toll",
      "violations": 245,
      "severity_score": 9.8,
      "primary_violation": "HELMET_NOT_WORN",
      "recommendation": "Increase CCTV coverage and enforcement"
    }
  ]
}
```

---

## Error Handling

All endpoints return error responses in this format:

```json
{
  "status": "error",
  "message": "Descriptive error message",
  "error_code": "ERROR_CODE"
}
```

### Common Error Codes

| Code | Status       | Description           |
| ---- | ------------ | --------------------- |
| 400  | Bad Request  | Invalid parameters    |
| 404  | Not Found    | Resource not found    |
| 500  | Server Error | Internal server error |

---

## Rate Limiting

- **Limit**: 1000 requests per hour per IP
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

---

## Examples

### Complete Workflow

1. **Upload image for violation detection**

```bash
curl -X POST "http://localhost:8000/api/violations/detect" \
  -F "file=@street_image.jpg" \
  -F "latitude=28.7041" \
  -F "longitude=77.1025" \
  -F "location_name=NH-48 Toll"
```

2. **Issue E-challan for detected violation**

```bash
curl -X POST "http://localhost:8000/api/challan/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "violation_id": 1,
    "owner_name": "Owner Name",
    "owner_phone": "+919876543210",
    "owner_email": "owner@email.com",
    "registration_number": "DL-01AB1234"
  }'
```

3. **Check analytics for the location**

```bash
curl "http://localhost:8000/api/analytics/summary?days=7"
```

---

## SDKs & Client Libraries

### Python Example

```python
import requests

API_URL = "http://localhost:8000/api"

# Detect violations
with open("image.jpg", "rb") as f:
    response = requests.post(
        f"{API_URL}/violations/detect",
        files={"file": f},
        data={
            "latitude": 28.7041,
            "longitude": 77.1025,
            "location_name": "NH-48 Toll"
        }
    )
    print(response.json())
```

---

## Support

For API issues or questions:

- GitHub Issues: [Repository Issues]
- Email: support@trafficviolationdetection.ai
- Documentation: [Full docs]
