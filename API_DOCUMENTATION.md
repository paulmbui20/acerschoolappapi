# Acer School App API Documentation

This document provides detailed information about the API endpoints, request formats, response structures, and examples for the Acer School App API.

## Base URL

All API endpoints are relative to the base URL:

```
http://localhost:8000/
```

When deployed, replace `localhost:8000` with your actual domain.

## Authentication

Currently, the API implements rate limiting but does not require authentication for read operations. The API uses Django REST Framework's built-in throttling mechanisms:

- Anonymous users: 60 requests per hour
- Authenticated users: Default Django REST Framework rate limits

## Common Response Formats

All API responses are returned in JSON format. Successful responses typically have HTTP status code 200 and contain the requested data.

Error responses include appropriate HTTP status codes (4xx for client errors, 5xx for server errors) and a JSON body with error details.

## API Endpoints

### 1. Grades API

#### GET /sample/grades/

Retrieve a list of all grades with their score ranges, points, and comments.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_size | int  | No       | Number of results per page |
| page      | int  | No       | Page number |

**Response:**

```json
{
  "overall_grades": [
    {
      "grade_letter": "A",
      "min_score": 80.0,
      "max_score": 100.0,
      "points": 12,
      "comment": "Excellent"
    },
    {
      "grade_letter": "A-",
      "min_score": 75.0,
      "max_score": 79.9,
      "points": 11,
      "comment": "Very Good"
    },
    // Additional grades...
  ]
}
```

### 2. Subjects API

#### GET /sample/subjects/

Retrieve a list of all subjects with their codes and names.

**Query Parameters:**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| search    | string | No       | Search term for filtering subjects by name or code |
| page_size | int    | No       | Number of results per page |
| page      | int    | No       | Page number |

**Response:**

```json
{
  "subjects": [
    {
      "subject_code": "MATH",
      "name": "Mathematics"
    },
    {
      "subject_code": "ENG",
      "name": "English"
    },
    // Additional subjects...
  ]
}
```

### 3. KCSE Papers API

#### GET /sample/kcse-papers/

Retrieve all KCSE subjects with their associated papers, including paper names, maximum scores, and percentage weights.

**Response:**

```json
{
  "subjects": [
    {
      "subject_code": "MATH",
      "name": "Mathematics",
      "papers": [
        {
          "paper_name": "Paper 1",
          "max_score": 100,
          "percentage_weight": 50.0
        },
        {
          "paper_name": "Paper 2",
          "max_score": 100,
          "percentage_weight": 50.0
        }
      ]
    },
    // Additional subjects with their papers...
  ]
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages in case of errors:

- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server-side error

Error response format:

```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Caching

The API implements Redis caching to improve performance. Responses are cached for 15 minutes with cache invalidation based on request parameters.

Cache headers are included in the response to indicate cache status:

- `Cache-Control`: Indicates caching directives
- `Vary`: Indicates which request headers were used for caching

## Performance Considerations

1. **Use Pagination**: For endpoints that return potentially large datasets, use the `page` and `page_size` parameters to limit the amount of data returned.

2. **Efficient Filtering**: Use the `search` parameter to filter results on the server side rather than retrieving all data and filtering client-side.

3. **Caching**: The API implements server-side caching, but consider implementing client-side caching for frequently accessed data that doesn't change often.

## Examples

### Example 1: Retrieving Grades

**Request:**

```
GET /sample/grades/?page=1&page_size=5
```

**Response:**

```json
{
  "overall_grades": [
    {
      "grade_letter": "A",
      "min_score": 80.0,
      "max_score": 100.0,
      "points": 12,
      "comment": "Excellent"
    },
    {
      "grade_letter": "A-",
      "min_score": 75.0,
      "max_score": 79.9,
      "points": 11,
      "comment": "Very Good"
    },
    {
      "grade_letter": "B+",
      "min_score": 70.0,
      "max_score": 74.9,
      "points": 10,
      "comment": "Good"
    },
    {
      "grade_letter": "B",
      "min_score": 65.0,
      "max_score": 69.9,
      "points": 9,
      "comment": "Above Average"
    },
    {
      "grade_letter": "B-",
      "min_score": 60.0,
      "max_score": 64.9,
      "points": 8,
      "comment": "Average"
    }
  ]
}
```

### Example 2: Searching for Subjects

**Request:**

```
GET /sample/subjects/?search=math
```

**Response:**

```json
{
  "subjects": [
    {
      "subject_code": "MATH",
      "name": "Mathematics"
    }
  ]
}
```

### Example 3: Retrieving KCSE Papers for a Subject

**Request:**

```
GET /sample/kcse-papers/
```

**Response (partial):**

```json
{
  "subjects": [
    {
      "subject_code": "MATH",
      "name": "Mathematics",
      "papers": [
        {
          "paper_name": "Paper 1",
          "max_score": 100,
          "percentage_weight": 50.0
        },
        {
          "paper_name": "Paper 2",
          "max_score": 100,
          "percentage_weight": 50.0
        }
      ]
    }
  ]
}
```

## Future Enhancements

1. **Authentication**: Implement JWT or OAuth2 authentication for secure API access
2. **Write Operations**: Add endpoints for creating, updating, and deleting resources
3. **Versioning**: Implement API versioning to ensure backward compatibility
4. **Documentation**: Integrate Swagger/OpenAPI for interactive API documentation
5. **Filtering**: Enhance filtering capabilities with more advanced query parameters
