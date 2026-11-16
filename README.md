# MyAssetStore

A free catalog of digital assets.

### Tech Stack
- Django
- Django REST Framework
- React (planned)

Currently, the project consists of a backend API. The frontend will be developed using React in the future.

### API Endpoints

| Endpoint | Description |
|---|---|
| `/asset/` | List all assets |
| `/asset/<id>/` | Retrieve a specific asset |
| `/register/` | Register a new account |
| `/login/` | Log in to an account |
| `/profile/` | Retrieve and update the user profile |

### Asset Query Parameters

- `?category=<categoryId>` — Filter assets by category.
- `?publisher=<publisherId>` — Filter assets by publisher.
- `?search=<query>` — Search assets by title or description.
- `?ordering=title` — Sort by title (A–Z).
- `?ordering=-title` — Sort by title (Z–A).
- `?ordering=created_at` — Sort by creation date (oldest first).
- `?ordering=-created_at` — Sort by creation date (newest first).

### Profile Model

A profile is automatically created when a user registers and is linked to their account.

The profile includes:
- An avatar.
- A list of specializations.

Available specializations are predefined and can also be managed through the Django admin panel.

### Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/wen3x/MyAssetStore.git
cd MyAssetStore
```

**2. Create and activate a virtual environment**

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root, copy the variables from `.env.example`, and provide your own values.

**5. Apply database migrations**

```bash
python manage.py migrate
```

**6. (Optional) Create a superuser**

```bash
python manage.py createsuperuser
```

**7. Run the development server**

```bash
python manage.py runserver
```