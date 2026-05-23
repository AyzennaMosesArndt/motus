CREATE TABLE users (
  id                  uuid PRIMARY KEY REFERENCES auth.users(id),
  email               text,
  primary_sport       text,
  sport_subcategory   text,
  preferred_distances text[],
  interests           text[],
  onboarded_at        timestamptz
);
