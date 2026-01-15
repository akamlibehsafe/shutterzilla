_This document outlines suggested data models for the ShutterZilla platform. These are recommendations and can be adapted during implementation._

# Data Models (Suggested)

## 1. User Model

| Field | Type | Description |
|---|---|---|
| `id` | `uuid` | Primary key. |
| `email` | `string` | User's email address (must be unique). |
| `password_hash` | `string` | Hashed password. |
| `name` | `string` | User's display name. |
| `avatar_url` | `string` | URL to the user's profile picture. |
| `role` | `enum` | User role (`user`, `admin`). Defaults to `user`. |
| `email_verified_at` | `timestamp` | Timestamp of when the user verified their email. Null if not verified. |
| `created_at` | `timestamp` | Timestamp of account creation. |
| `last_login_at` | `timestamp` | Timestamp of the last login. |

## 2. Scraper: CameraListing Model

| Field | Type | Description |
|---|---|---|
| `id` | `uuid` | Primary key. |
| `source` | `enum` | The source of the listing (e.g., `buyee`, `ebay`). |
| `source_id` | `string` | The original ID of the listing on the source platform. |
| `title` | `string` | The title of the listing. |
| `url` | `string` | The URL to the original listing. |
| `image_url` | `string` | The URL of the primary image. |
| `price` | `decimal` | The price of the camera. |
| `currency` | `string` | The currency of the price (e.g., `USD`, `JPY`). |
| `condition` | `enum` | The condition of the camera (e.g., `mint`, `excellent`, `good`, `fair`, `poor`). |
| `is_sold` | `boolean` | Whether the camera has been marked as sold. Defaults to `false`. |
| `posted_at` | `timestamp` | The timestamp when the listing was posted. |
| `scraped_at` | `timestamp` | The timestamp when the listing was last scraped. |

## 3. Scraper: SavedSearch Model

| Field | Type | Description |
|---|---|---|
| `id` | `uuid` | Primary key. |
| `user_id` | `uuid` | Foreign key to the `User` model. |
| `name` | `string` | A user-defined name for the saved search. |
| `query_params` | `json` | A JSON object containing the search parameters (keywords, filters, etc.). |
| `created_at` | `timestamp` | Timestamp of when the search was saved. |

## 4. Collection: CollectionCamera Model

| Field | Type | Description |
|---|---|---|
| `id` | `uuid` | Primary key. |
| `user_id` | `uuid` | Foreign key to the `User` model. |
| `status` | `enum` | The status of the camera in the collection (`owned`, `wishlist`). |
| `brand` | `string` | The brand of the camera. |
| `model` | `string` | The model of the camera. |
| `year` | `integer` | The year of manufacture. |
| `serial_number` | `string` | The camera's serial number (optional). |
| `condition` | `enum` | The user's assessment of the camera's condition. |
| `purchase_price` | `decimal` | The price the user paid for the camera (for `owned` items). |
| `current_value` | `decimal` | The estimated current value of the camera. |
| `notes` | `text` | User's personal notes about the camera (optional). |
| `image_url` | `string` | URL of a user-uploaded image of the camera (optional). |
| `added_at` | `timestamp` | Timestamp of when the camera was added to the collection. |
