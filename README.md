# culturemapp
Culturemapp is an interactive, dynamic web app mapping over 400 cultural venues in the city of Milan, Italy. 

The dataset and the methodolody for the definition of what counts as a "cultural venue" were gathered and developed with the support of a team from the Municipality of Milan. 

## CS50W requirements

### Distinctiveness and complexity

While some functionalities (e.g. adding a favorite venue) are strongly reminiscent of other CS50w projects such as "Network", most of core of this app has nothing to do with any other previous project. Additionally, most features are far more complex. 

E.g.:

* the home page is in fact a geographical rendering of the venues object instances from the db
* two type of users are introduced (on top of the Admin layer) - something that is not present in any other project
  * the venue manager user type is activated only by the admin
* user authentication is in two-steps via confirmation email
* ...

## How to run

The project can be run by:

1. installing all the required dependencies as detailed in `requirements.txt`
2. executing `python manage.py runserver` in CLI.

## Live demo

A live demo was deployed to Heroku and can be seen by clicking on [this link](https://culturemapp.herokuapp.com). Some features such as geolocation may need to be enabled in your browser or not be fully functional due to Heroku's security limitations.

## Structure

### Homepage

The homepage is an interactive map built in python via `folium` and rendered as a `Leaflet`. 

**All user types**, whether registered or unregistered can: 

* zoom in or out 
* filter venues by category
* search venues by venue name
* see venues next to their location when geolocation is enabled.

Clicking on a venue marker will display a tooltip with the venue's basic information. The tooltip itself will link to the venue's detail page, which includes the venues latest news and events.

**Admin** users can refresh the map after having modified it by adding, removing, editing venues or categories by clicking on "Aggiorna".

The homepage can be reached from any other page in the webapp by clicking on the CultureMappMilano link in the navigation bar.

### Registration and user types

Users can register as **standard users** or as **venues managers** via the **Iscriviti** link on the navigation bar. 

#### Unregistered users

**Unregistered users**, in addition to navigating the map, can:

* see the latest news (**Notizie** in the navigation bar)
* see the latest events (**Eventi** in the navigation bar)

#### Registered users

A **registered user** will be able to:

* save his favorite venues and retrieve them or modify the list by clicking on **Preferiti** in the navigation bar
* have access to their own **profile page**.

In order to register a user will have to provide a valid confirmation email and confirm their email address by clicking on the link. 

#### Venue managers

A **venue manager** will be able to: 

* **edit** the venues they manage (if the address is changed the map will update itself provided the address corresponds to valid coordinates)
* **post news** for the venues they manage
* **post events** for the venues they manage.

These features can be accessed from the dropdown menu under the venue managers profile button.

*Venue managers have to be authorized by the Admin in order to gain access.*

## File descriptions

Description of main files added.

* `constants.py` Contains CONSTANTS used in creating the map (e.g. a dictionary for the html rendering of markers

* `forms.py` forms for editing venues, posting news and posting events 
* `static/venues`
  * `assets` Material Kit CSS and JS
  * `edit.js` Venue editing
  * `follow.js` Venue add to favorites
  * `readmore.js` Adds read more/readless button when needed
  * `styles.css` Self-explanatory
* `utils.py` Contains functions utilized in `views.py` e.g.`make_map`, `find_coordinates`
* `tokens.py` Generates account activation tokens
