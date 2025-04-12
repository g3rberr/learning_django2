# Learning Django 2

This project is a hands‑on exercise in Django fundamentals, covering template integration, authentication, cart logic, OAuth, testing, and Stripe payments.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Project Structure](#project-structure)  
7. [Testing](#testing)  
8. [Future Work](#future-work)  

---

## Overview

`learning_django2` is a practice repository where I implemented core Django concepts, from setting up templates and user authentication to more advanced flows like cart management and OAuth integration. I also explored writing my first tests and integrating Stripe for payment processing :contentReference[oaicite:0]{index=0}.

---

## Features

- **Template Integration**: Modular HTML templates with Django’s templating engine.  
- **User Authentication**: Registration, login, logout, and profile management.  
- **Cart Logic**: Add/remove items, view cart summary, and persist cart state.  
- **OAuth**: Third‑party login via Google (or other providers).  
- **Stripe Payments**: Secure payment flow for cart checkout.  
- **Testing**: Initial unit and integration tests to validate models and views.  

---

## Tech Stack

- **Backend**: Django 2.x  
- **Frontend**: HTML5, CSS3, JavaScript  
- **Database**: SQLite (default)  
- **Payments**: Stripe API  
- **Authentication**: Django’s built‑in auth + `django-allauth` (for OAuth)  
- **Testing**: Django’s `TestCase` framework  

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/g3rberr/learning_django2.git
   cd learning_django2

    Create & activate virtualenv

    python3 -m venv venv
    source venv/bin/activate

Install dependencies

    pip install -r requirements.txt

Run migrations

    python manage.py migrate

Create a superuser (optional)

    python manage.py createsuperuser

Start the server

    python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser.

## Usage

Browse products and add them to your cart.

Register or log in to proceed to checkout.

Use OAuth (e.g., Google) for quick login.

Complete a purchase via Stripe’s secure payment form.

## Project Structure

    learning_django2/
      ├── products/       # Product models, views, templates
      ├── orders/         # Order processing & cart logic
      ├── users/          # Custom user and authentication
      ├── common/         # Shared utilities & context processors
      ├── store/          # Main storefront app
      ├── static/         # CSS, JS, images
      ├── templates/      # Base and app templates
      ├── manage.py
      ├── requirements.txt

## Testing

I’ve started writing tests for core functionality:

    python manage.py test

Current coverage includes:

    Model validations

    View responses for key URLs

    Cart addition/removal logic

## Future Work

    Expand test coverage (edge cases, error flows).

    Add caching (e.g., Redis) for performance.

    Refine UI/UX with modern frontend (React/Vue).

    Dockerize the application for easier deployment.
