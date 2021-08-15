<img width="1678" alt="Project_Header" src="https://user-images.githubusercontent.com/83195797/124826906-3e31be80-df2a-11eb-9135-7eee4c7755ed.png">

Neighborhood Lost Pets was inspired by wanting a way for pet lovers to come together to support and help each other in their neighborhood. A place where neighbors can report and help find lost pets. Using Google Maps API, when a pet is reported missing, a new marker with the last seen location will be placed on the map with information about the pet and pet owner. Once logged in, members can search for lost pets in their neighborhood and connect with the respective pet owners.

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future Features](#future-features)
* [Installation](#installation)
* [Credits](#credits)

## <a name="tech-stack"></a>Tech Stack
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

## <a name="features"></a>Features
### Landing Page
* Users login and registration built with flask-login module for authentication management.
* Password hashing was implemented using bcrypt.

<img width="1678" alt="landing2" src="static/img/lost-pet.gif">

### Main Dashboard
* After logging in, users land on this main dashboard that was built with Jinja templating and Flask-SQLAlchemy for database queries. Here users can:
> 1. Report a lost pet
> 2. Search for lost pets
> 3. Update when a pet is found
* To search for lost pets in a neighborhood:
> 1. Users can enter an address or even just a location. Built with Google Maps API and their geocoding capabilities.
> 2. Users location can also be detected automatically. Built with the geolocation functionality.

![main-dash](https://user-images.githubusercontent.com/83195797/129280263-0c91a0cb-a781-49ee-93e6-ca5252c451aa.png)

### Markers - Lost Pet Info
* The data from each marker on the map uses Javascript AJAX request to jsonify the data
> Once a lost pet has been reported missing, a new marker will be placed on the map.
> When a marker is clicked, users can see more informaion about the pet and how to contact the pet owner.

![marker-pet](https://user-images.githubusercontent.com/83195797/129281267-5bb412f7-c85f-43bf-92b1-532aca654e42.png)

#### Night Mode
![marker-pet-night](https://user-images.githubusercontent.com/83195797/129281355-13a345aa-3023-40f1-86fd-00fcd752c910.png)

## <a name="future-features"></a>Future Features:
The roadmap for this project includes features such as:
> *  [x] Password hashing (√ Done)
> *  [ ] Leveraging React components
> *  [ ] Dedicated pet owner's section for all things 'my pet'
> *  [ ] Messaging capability within the app
> *  [ ] Pin nearby vet clinics and police stations

## <a name="installation"></a>Installation
To run Neighborhood Lost Pets app on your machine:

#### Clone this repo:
> ```
> https://github.com/yardnas/Neighborhood-Lost-Pets.git
> ```

#### Install PostgresQL

#### Create and launch a virual environment in your Neighborhood Lost Pets directory:
> ```
> virtual env
> source env/bin/activate
> ```

#### Install the dependencies:
> ```pip install -r requirements.txt```

#### Seed the app with starter data:
> ```python3 seed.py```

#### Run the app:
> ```python3 server.py```

#### Access the app via browser:
> ```'localhost:5000/'```

## <a name="credits"></a>Credits
* Google (Google Maps API)
* Unsplash (Images)
* Dreamstime (Logo)


