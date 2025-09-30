
# 🌌 StarPythonWars

**StarPythonWars** is a client to interact with the [Star Wars API (SWAPI)](https://swapi.py4e.com/).  
It allows you to query and manipulate information about films, characters, planets, starships, and vehicles from the Star Wars universe.

---

## 🚀 Main features
- Client to connect to the Star Wars API.
- Data models (`Film`, `People`, `Planet`, `Starship`, `Vehicle`) with specific methods.
- Customised error handling 
- Automated tests included.
- Organised and extensible code.
```text
📁 Project Structure
StarPythonWars/
│
├── client/                 # API client and utilities
│   ├── __init__.py
│   ├── client.py          # Main API client class
│   ├── resource.py        # Abstract base class for API resources
│   └──  url.py            # API endpoint configuration
│             
│
├── models/                # Data models
│   ├── __init__.py
│   ├── errors.py         # Custom exception classes
│   ├── people.py         # People/Character model
│   ├── planet.py         # Planet model
│   ├── starship.py       # Starship model
│   ├── vehicle.py        # Vehicle model
│   └── film.py           # Film model
│
├── test/                  # Unit tests
│   ├── __init__.py
│   └── tests_client.py   # Tests for API client
├── user.py # Interactive CLI application
└── README.md                   
```
## 🛠️ Install

git clone https://github.com/usuario/StarPythonWars.git

pip install -r requirements.txt
##
The application can be tested by using the user.py class.


