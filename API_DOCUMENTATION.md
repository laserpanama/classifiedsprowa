# Classifieds Pro API Documentation

This document provides a detailed reference for the Classifieds Pro backend API.

## Base URL

The base URL for all API endpoints is `/api`.

---

## Accounts

The Accounts API is used to manage the `wanuncios.com` user accounts that the system will use to post ads.

### `POST /accounts/`

- **Description:** Creates a new wanuncios.com account in the system.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "wanuncios_password": "secure_password123"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "id": "a-unique-uuid",
    "email": "user@example.com",
    "is_active": true
  }
  ```

### `GET /accounts/`

- **Description:** Retrieves a list of all accounts in the system.
- **Response (200 OK):**
  ```json
  [
    {
      "id": "a-unique-uuid",
      "email": "user@example.com",
      "is_active": true
    }
  ]
  ```

### `GET /accounts/{account_id}`

- **Description:** Retrieves a single account by its ID.
- **Response (200 OK):**
  ```json
  {
    "id": "a-unique-uuid",
    "email": "user@example.com",
    "is_active": true
  }
  ```

### `PATCH /accounts/{account_id}`

- **Description:** Updates an account's details.
- **Request Body:**
  ```json
  {
    "email": "new_email@example.com",
    "is_active": false
  }
  ```
- **Response (200 OK):** The updated account object.

### `DELETE /accounts/{account_id}`

- **Description:** Deletes an account from the system.
- **Response (204 No Content):** An empty response on success.

---

## Ads

The Ads API is used to manage the ad templates that will be posted.

### `POST /ads/`

- **Description:** Creates a new ad template.
- **Request Body:**
  ```json
  {
    "account_id": "the-uuid-of-the-account-to-use",
    "title": "My Awesome Ad",
    "description": "A great description of what I'm selling.",
    "category": "Contactos",
    "subcategory": "Relaciones Ocasionales",
    "province": "Panamá",
    "zone": "Panama City",
    "price": 50.00
  }
  ```
- **Response (200 OK):** The created ad object.

### `GET /ads/`

- **Description:** Retrieves a list of all ad templates.
- **Response (200 OK):** A list of ad objects.

### `POST /ads/generate-text`

- **Description:** Generates ad description text using AI.
- **Request Body:**
  ```json
  {
    "prompt": "A catchy title for a great product"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "generated_text": "This is the AI-generated ad description..."
  }
  ```

### `POST /ads/{ad_id}/publish`

- **Description:** Starts a background task to post an ad to wanuncios.com.
- **Response (200 OK):**
  ```json
  {
    "message": "Ad publishing has been started in the background."
  }
  ```

---

## Schedules

The Schedules API is used to manage the automatic republishing of ads.

### `POST /schedules/`

- **Description:** Creates a new republishing schedule for an ad.
- **Request Body:**
  ```json
  {
    "ad_id": "the-uuid-of-the-ad-to-schedule",
    "republish_interval_hours": 24
  }
  ```
- **Response (200 OK):** The created schedule object.

### `GET /schedules/`

- **Description:** Retrieves a list of all schedules.
- **Response (200 OK):** A list of schedule objects.

### `PATCH /schedules/{schedule_id}`

- **Description:** Updates a schedule (e.g., to toggle it on or off).
- **Request Body:**
  ```json
  {
    "is_active": false
  }
  ```
- **Response (200 OK):** The updated schedule object.

### `DELETE /schedules/{schedule_id}`

- **Description:** Deletes a schedule.
- **Response (204 No Content):** An empty response on success.
