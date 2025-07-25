# API Examples

## Getting Events

### Get Events for Next Week (Default)
```bash
curl "http://localhost:8000/api/Calendar"
```

**Response**:
```json
[
  {
    "id": 1,
    "start": "2025-07-25T10:00:00",
    "name": "Team Meeting",
    "note": "Weekly team sync",
    "type": 1
  }
]
```

### Get Events from Today
```bash
curl "http://localhost:8000/api/Calendar?tf_days=-1&after_days=0"
```

### Get Events for Specific Date Range
```bash
curl "http://localhost:8000/api/Calendar?tf_days=1&after_days=7"
```

## Filtering Events

### Get Events by IDs
```bash
curl "http://localhost:8000/api/Events?ids=1,2,3"
```

### Get Events by Type
```bash
curl "http://localhost:8000/api/Events?type=1,2"
```

**Event Types**:
- `0`: Default
- `1`: Meetings/Planning
- `2`: Development/Technical
- `3`: Demo/Presentations
- `4`: Informal Events

### Combined Filters
```bash
curl "http://localhost:8000/api/Events?ids=1,2&type=1"
```

## Creating Events

### Create Event with Current Time
```bash
curl -X POST "http://localhost:8000/api/Event" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "New Meeting",
    "Note": "Important discussion",
    "Type": 1
  }'
```

### Create Event with Specific Time
```bash
curl -X POST "http://localhost:8000/api/Event" \
  -H "Content-Type: application/json" \
  -d '{
    "Start": 1721822400,
    "Name": "Scheduled Meeting", 
    "Note": "Meeting at specific time",
    "Type": 1
  }'
```

**Response**:
```json
{
  "message": "Success created event id 42"
}
```

## Python Examples

### Using Requests Library

```python
import requests
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:8000/api"

# Get events
response = requests.get(f"{BASE_URL}/Calendar")
events = response.json()
print(f"Found {len(events)} events")

# Create new event
new_event = {
    "Name": "Python Generated Event",
    "Note": "Created via Python script",
    "Type": 2
}

response = requests.post(f"{BASE_URL}/Event", json=new_event)
result = response.json()
print(result["message"])

# Get events by type
response = requests.get(f"{BASE_URL}/Events", params={"type": "2"})
dev_events = response.json()
print(f"Development events: {len(dev_events)}")
```

### Using HTTPX (Async)

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Get calendar events
        response = await client.get("http://localhost:8000/api/Calendar")
        events = response.json()
        
        for event in events:
            print(f"Event: {event['name']} at {event['start']}")

asyncio.run(main())
```

## JavaScript Examples

### Using Fetch API

```javascript
// Get events
fetch('http://localhost:8000/api/Calendar')
  .then(response => response.json())
  .then(events => {
    console.log('Events:', events);
    events.forEach(event => {
      console.log(`${event.name} - ${event.start}`);
    });
  });

// Create event
const newEvent = {
  Name: "JavaScript Event",
  Note: "Created from browser",
  Type: 1
};

fetch('http://localhost:8000/api/Event', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(newEvent)
})
.then(response => response.json())
.then(result => console.log(result.message));
```

### Using Axios

```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Get events with date range
api.get('/Calendar', {
  params: {
    tf_days: -1,
    after_days: 7
  }
})
.then(response => {
  console.log('Events:', response.data);
})
.catch(error => {
  console.error('Error:', error.response.data);
});
```

## Common Use Cases

### Daily Agenda
```bash
# Get today's events
curl "http://localhost:8000/api/Calendar?tf_days=-1&after_days=0"
```

### Weekly Planning
```bash
# Get next week's events
curl "http://localhost:8000/api/Calendar?tf_days=0&after_days=0"
```

### Meeting Reports
```bash
# Get all meetings (type 1)
curl "http://localhost:8000/api/Events?type=1"
```

### Development Tasks
```bash
# Get all development events (type 2)
curl "http://localhost:8000/api/Events?type=2"
```
