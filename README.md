# Globussoft Assignment

## Overview

This repository contains solutions for two tasks:

### Task 1: Amazon Laptop Scraper

A Python-based web scraper that extracts laptop listings from Amazon India.

The scraper collects:

* Product Title
* Price
* Rating
* Image URL
* Ad / Organic Result

The extracted data is stored in a timestamped CSV file.

### Task 2: Face Authentication API

A FastAPI-based application that performs face verification using DeepFace.

The API:

* Accepts two face images
* Detects faces in both images
* Compares facial embeddings
* Calculates similarity score
* Returns:

  * Same Person / Different Person result
  * Similarity Score
  * Face Bounding Boxes

---

## Project Structure

```text
Globussoft-Assignment/
│
├── task1/
│   └── amazon_scraper.py
│
├── task2/
│   └── app.py
│
├── sample_images/
│   ├── same_person_1.jpg
│   ├── same_person_2.jpg
│   ├── different_person_1.jpg
│   └── different_person_2.jpg
│
├── requirements.txt
└── README.md
```

---

## Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Task 1: Run Amazon Scraper

```bash
python task1/amazon_scraper.py
```

Output:

```text
amazon_laptops_YYYYMMDD_HHMMSS.csv
```

---

## Task 2: Run Face Authentication API

Start the FastAPI server:

```bash
uvicorn task2.app:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoint

### POST /verify-faces

Uploads two face images and returns:

* Verification Result
* Similarity Score
* Bounding Boxes

Example Response:

```json
{
  "verification_result": "different person",
  "similarity_score": 0.0535,
  "bounding_boxes": {
    "image1": {
      "x": 64,
      "y": 30,
      "w": 67,
      "h": 67
    },
    "image2": {
      "x": 61,
      "y": 29,
      "w": 70,
      "h": 70
    }
  }
}
```



## Technologies Used

* Python
* Requests
* BeautifulSoup
* Pandas
* FastAPI
* DeepFace
* OpenCV
* TensorFlow

