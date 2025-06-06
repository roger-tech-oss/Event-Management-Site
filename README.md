# Event Management System (Django + MySQL)

## 📋 Project Overview
This **Event Management System** is a full-stack web application developed using **Django** and **MySQL** that allows users to explore, register, and manage events. It includes both frontend and backend functionalities with authentication, event creation/editing, RSVP, and a mock payment system using Razorpay.

## ✅ Features & Functionalities

### User Functionalities
- 🔐 **User Authentication**: Register, login, logout.
- 📅 **View Events**: Browse a list of upcoming events with filters (search, date, venue).
- 📝 **Event Details**: View detailed information about each event.
- 🎟️ **Event Registration**:
  - Choose number of tickets.
  - Make a payment (mock Razorpay or real integration ready).
  - Receive ticket via email (PDF).
- 📜 **RSVP System**: Confirm attendance to events.
- 📊 **User Dashboard**: View events created by the user.

### Admin/Organizer Functionalities
- ➕ **Create Events**: Title, description, date/time, price, venue, and image.
- 🛠️ **Edit & Delete Events**: Manage events only by the creator (organizer).
- 📧 **Ticket Email**: Sends automatic ticket as PDF after payment.

## 🛠️ Technologies Used
- **Backend**: Django 5.2.1 (Python 3.13.3)
- **Frontend**: HTML, CSS (Bootstrap optionally)
- **Database**: MySQL
- **Payment Gateway**: Razorpay (test/dummy mode integrated)
- **Emailing**: Django EmailMessage + `xhtml2pdf` for PDF generation
- **Session Management**: Django session for temporary order storage
- **Deployment**: Development server (use Gunicorn/Nginx for production)

## 🗂️ Modules & Files

### Models (`models.py`)
- `Venue`: Name, address, capacity.
- `Event`: Linked to venue and user; includes title, date, price, image.
- `Registration`: Links user and event with ticket count.

### Views (`views.py`)
- `home`: Displays list of events.
- `event_detail`: Shows detailed info about a single event.
- `register_for_event`: Initiates dummy checkout and saves session.
- `payment_success`: Handles dummy payment and confirms registration.
- `create_event`, `edit_event`, `delete_event`: Organizer event management.
- `rsvp_event`: RSVP to events.
- `user_dashboard`: View created events.
- `send_ticket_email`: Generates and sends PDF ticket.

## 🔒 Security & Access Control
- Only logged-in users can register, RSVP, and create/edit events.
- Events can only be edited/deleted by their respective organizers.

## 📥 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/event-management-django.git
   cd event-management-django
   ```

2. **Create virtual environment & install dependencies**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure `.env` or `settings.py` for email & Razorpay keys**

4. **Apply migrations and run server**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

5. **Access the app**
   Visit: `http://127.0.0.1:8000/`

## 📧 Contact
For issues or collaboration, feel free to reach out via georgebiby002@gmail.com.
