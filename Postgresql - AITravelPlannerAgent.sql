CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "full_name" varchar,
  "email" varchar UNIQUE,
  "password_hash" varchar,
  "avatar_url" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "user_preferences" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "preferred_currency" varchar,
  "budget_min" decimal,
  "budget_max" decimal,
  "favorite_country" varchar,
  "favorite_food" varchar,
  "hotel_star" int,
  "travel_style" varchar,
  "transportation_preference" varchar,
  "created_at" timestamp
);

CREATE TABLE "trips" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "title" varchar,
  "destination" varchar,
  "start_date" date,
  "end_date" date,
  "budget" decimal,
  "total_estimated_cost" decimal,
  "status" varchar,
  "created_at" timestamp
);

CREATE TABLE "trip_days" (
  "id" uuid PRIMARY KEY,
  "trip_id" uuid,
  "day_number" int,
  "title" varchar,
  "description" text
);

CREATE TABLE "activities" (
  "id" uuid PRIMARY KEY,
  "trip_day_id" uuid,
  "place_name" varchar,
  "category" varchar,
  "start_time" time,
  "end_time" time,
  "estimated_cost" decimal,
  "latitude" decimal,
  "longitude" decimal,
  "notes" text
);

CREATE TABLE "calendar_events" (
  "id" uuid PRIMARY KEY,
  "activity_id" uuid,
  "event_title" varchar,
  "event_date" date,
  "start_time" time,
  "end_time" time,
  "reminder" boolean
);

CREATE TABLE "chat_sessions" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "title" varchar,
  "created_at" timestamp
);

CREATE TABLE "chat_messages" (
  "id" uuid PRIMARY KEY,
  "session_id" uuid,
  "role" varchar,
  "message" text,
  "created_at" timestamp
);

CREATE TABLE "saved_places" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "name" varchar,
  "country" varchar,
  "city" varchar,
  "latitude" decimal,
  "longitude" decimal,
  "category" varchar,
  "notes" text
);

CREATE TABLE "currency_history" (
  "id" uuid PRIMARY KEY,
  "base_currency" varchar,
  "target_currency" varchar,
  "exchange_rate" decimal,
  "fetched_at" timestamp
);

CREATE TABLE "weather_cache" (
  "id" uuid PRIMARY KEY,
  "city" varchar,
  "country" varchar,
  "weather" varchar,
  "temperature" decimal,
  "humidity" decimal,
  "fetched_at" timestamp
);

CREATE TABLE "documents" (
  "id" uuid PRIMARY KEY,
  "title" varchar,
  "file_name" varchar,
  "source" varchar,
  "uploaded_at" timestamp
);

CREATE TABLE "tool_logs" (
  "id" uuid PRIMARY KEY,
  "trip_id" uuid,
  "tool_name" varchar,
  "input" text,
  "output" text,
  "status" varchar,
  "execution_time_ms" int,
  "created_at" timestamp
);

ALTER TABLE "user_preferences" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "trips" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "trip_days" ADD FOREIGN KEY ("trip_id") REFERENCES "trips" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "activities" ADD FOREIGN KEY ("trip_day_id") REFERENCES "trip_days" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "calendar_events" ADD FOREIGN KEY ("activity_id") REFERENCES "activities" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "chat_sessions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "chat_messages" ADD FOREIGN KEY ("session_id") REFERENCES "chat_sessions" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "saved_places" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tool_logs" ADD FOREIGN KEY ("trip_id") REFERENCES "trips" ("id") DEFERRABLE INITIALLY IMMEDIATE;


