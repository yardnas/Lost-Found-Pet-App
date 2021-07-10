<img width="840" alt="Project_Header" src="https://user-images.githubusercontent.com/83195797/124826906-3e31be80-df2a-11eb-9135-7eee4c7755ed.png">

Neighborhood Lost Pets was inspired by wanting a way for pet lovers to come together to support and help each other in their neighborhood. A place where neighbors can report and help find lost pets. Using Google Maps API, when a pet is reported missing, a new marker with the last seen location will be placed on the map with information about the pet and pet owner. Once logged in, members can search for lost pets in their neighborhood and connect with the respective pet owners.

## Technologies
* Python
* Javascript
* HTML
* CSS
* Flask
* Jinja
* SQLAlchemy ORM
* jQuery
* AJAX
* PostgresQL
* Google Maps API

## Installation
To run Neighborhood Lost Pets app on your machine:

Clone this repo:
```
https://github.com/yardnas/Neighborhood-Lost-Pets.git
```

Install PostgresQL

Create and launch a virual environment in your Neighborhood Lost Pets directory:
```
virtual env
source env/bin/activate
```
Install the dependencies:
```pip install -r requirements.txt```

Seed the app with starter data:
```python3 seed.py```

Run the app:
```python3 server.py```

Access the app:
Go to ```'localhost:5000/'```

## Future Features:
The roadmap for this project includes features such as:
* Password hashing (next)
* Leveraging React components
* Dedicated pet owner's section for all things 'my pet'
* Messaging capability within the app
* Pin nearby vet clinics and police stations

## Credits
* Google (Google Maps API)
* Unsplash (Images)
* Dreamstime (Logo)


