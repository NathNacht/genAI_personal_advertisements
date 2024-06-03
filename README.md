# GenAI Personal Advertisements

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

This project leverages a database of customer, subscription plan, and promotion information from a telecommunications company to deploy user-specific advertisements using generative AI.

## 📦 Repo Structure

```
my_project/
│
├── .env
├── database.py
├── main.py
├── models.py
└── requirements.txt
```

## Database Structure

The database consists of several tables: `Customer`, `Subscription`, `Promotion`, `Advertisement`, and `Outcome`. Below is a visual representation of the database schema and it's flow.

### Entity-Relationship Diagram (ERD)

```plaintext
Customer       Subscription       Promotion       Advertisement       Outcome
--------       ------------       ---------       --------------      -------
| id      |    | id          |    | id      |     | id            |   | id        |
| name    |    | plan_name   |    | details |     | customer_id   |   | ad_id     |
| email   |    | features    |    | validity|     | promotion_id  |   | customer_id|
| demographic_info           |    | period  |     | subscription_id|   | timestamp |
| subscription_id            |                |     | generated_prompt|   | action    |
                            |                |     | generated_image |  |           |
                            |                |     | generated_text  |  |           |
                            |                |     | outcome         |  |           |


### Flow Overview

+-------------------+          +---------------------+          +--------------------+
|                   |          |                     |          |                    |
|    Customer       |          |    FastAPI          |          |  Generative AI     |
|                   |          |                     |          |                    |
+--------+----------+          +---------+-----------+          +---------+----------+
         |                             |                              |
         v                             v                              |
+--------+----------+          +-------+---------+          +---------+--------+
|                   |          |                 |          |                  |
|   Subscription    +---------->  Get Request    +---------->  Prompt Generator |
|                   |          |                 |          |                  |
+--------+----------+          +-------+---------+          +---------+--------+
         |                             |                              |
         v                             v                              v
+--------+----------+          +-------+---------+          +---------+--------+
|                   |          |                 |          |                  |
|    Promotion      +---------->  Generate Ad    +---------->  Image Generator  |
|                   |          |                 |          |                  |
+--------+----------+          +-------+---------+          +---------+--------+
         |                             |                              |
         v                             v                              v
+--------+----------+          +-------+---------+          +---------+--------+
|                   |          |                 |          |                  |
|   Advertisement   <----------+  Post Response  <----------+  Text Generator   |
|                   |          |                 |          |                  |
+--------+----------+          +-------+---------+          +---------+--------+
         |                             |                              |
         v                             v                              v
+--------+----------+          +-------+---------+          +---------+--------+
|                   |          |                 |          |                  |
|      Outcome      <----------+  Accept/Decline +<---------+  Feedback Loop   |
|                   |          |                 |          |                  |
+-------------------+          +-----------------+          +------------------+

## 🎮 Setup Instructions

### Step 1:

```
git clone https://github.com/yourusername/genAI_personal_advertisements.git
cd genAI_personal_advertisements
```

### Step 2:

```
pip install -r requirements.txt
```

### Step 3:

```
uvicorn main:app --reload
```

## 📌 Background

This team project was completed as part of the AI Boocamp at BeCode.org. Connect with the team behind the magic.

1. [Alice Mendes] (https://www.linkedin.com/in/alice-edcm/)
2. [Bear Revels](https://www.linkedin.com/in/bear-revels/)
2. [Daryoush Ghanbarpour](https://www.linkedin.com/in/daryoushghanbarpour/)
3. [Nathalie Nachtergaele](https://www.linkedin.com/in/nathalie-nachtergaele/)
4. [Yanina Andriienko](https://www.linkedin.com/in/yanina-andriienko-7a2984287/)