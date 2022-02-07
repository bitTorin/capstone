# Read Me  

## Intro

Welcome to City3D, a capstone project for CS50's Web Programming course. For this project, I focused on creating an accessible interface for citizens to view active construction projects in their city in a 3D environment. Currently, most construction dashboards rely on a standard 2D map and require a lot of additional web browsing to view the full picture of a building’s construction status. Renderings of the building, cost, competition date, and project updates are often found via disjointed information sources. City3D attempts to consolidate that information into a centralized dashboard improving the user’s experience journeying into the world of architecture and construction. As an architect, I felt that building this consumer facing application, through the utilization of emerging WebGL technologies, could alleviate many of the pain points that a citizen feels when they try to stay up to date with their locality’s current architectural projects.

## Distinctiveness and Complexity

This project is unique and complex in its implementation of a 3D maps environment to display geolocated pin markers for every active construction project in a city. After much trial and error with many Web GL platforms (Google Maps Web GL Beta, Cesium.JS, Unity, Unreal Engine, etc.), I settled on a Three.JS implementation with the Mapbox WebGL API to supply the base maps layer and Threebox, an open source plugin, to place .gltf files on location. This framework proved to be lightweight enough to run smoothly without experiencing the same client-side rendering limitations of the other WebGL frameworks without sacrificing design quality. These frameworks also allow significant customization methods.

In order to obtain the permit data that is displayed within the application, I also wrote some custom python scripts to retrieve a dataset for that city’s issued construction permit from within their databases. In this implementation, I have provided the scripts for two showcase cities, Austin and San Francisco. These datasets are both retrieved via a GET request to their respective Socrata database API’s.  The request returns a JSON file that is first converted into a pandas dataframe and then relayed into the proper Django model after undergoing proper formatting.

In completing this capstone, I’ve succeeding in building a mobile responsive application that relies on the model framework of a Django backend to store the permit information for hundreds of active construction permits. It also demonstrates a wide array of Javascript functionalities on the front end through the use of the Three.JS WebGL framework and event triggers on objects actions.

I hope you find this web application to be helpful. Thank you to the full CS50 team for creating this course, it has been full of learning and discovery! Below are a series of startup instructions to get the web application running locally. Good luck!

## Startup Instructions

Before running our application please ensure you have the latest versions of `python`, `pip`, and `Django` installed on your system.

### Step 1: Set up project

Clone this repository:
> git clone https://github.com/bitTorin/capstone.git

Create own virtual environment:
> python 3 -m venv venv
> source venv/bin/activate

Install project requirements:
> pip install -r requirements.txt

### Step 2: Define custom variables

In the base directory of our project folder, create a file titled `.env`. This should be in the same subdirectory as our `manage.py` file.

In the `.env` file copy and paste the following lines:
	> # SECURITY WARNING: keep the secret key used in production secret!
	> SECRET_KEY=<insert security key here>
	>
	> # SECURITY WARNING: don't run with debug turned on in production!
	> DEBUG=True
	>
	> # SOCRATA App Token
	> APP_TOKEN=<insert api key here>
	>
	> # MAPBOX App Token
	> MAPBOX_API=<insert api key here>

Now, we will generate a custom Django security key for you to run this application. In the terminal change your directory to this project's capstone directory and run the following command:

	> `python manage.py security_key`

The terminal will print a unique security key for you to copy. Paste the newly generated key into the `.env` file at the `SECURITY_KEY` variable.

Next we will need to create two API token for external services that will be used inside our application.

First, go to [Mapbox](https://account.mapbox.com/auth/signup/) to create an account. After completing the account creation, your user dashboard should show a `Default public token`. Copy this token and paste it into the `.env` file within the `MAPBOX_API` variable. This unique token is what will be used to load the maps on each webpage refresh. Please note there are only a certain number of free webpage loads before your account will start getting billed. Ensure you have read and understood the Mapbox Terms of Serivce regarding the quantity of free API requests provided before launching the application.

Second, go to [Socrata](https://evergreen.data.socrata.com/signup) and create an account. This account will be used to access a city's open data platform for building permits. After creating your account, access your API dashboard via `Edit Profile > Developer Settings`. Here you will create an App token. Sample name and description attributes might be:

	> Name: City3d
	> Description: API request for issued construction permits for various cities

Now that your token is created, we will copy and paste the `App Token` into the `.env` file.

Great, all of our custom variables have been defined!  

### Step 3: Launch application

Now it is time to launch our application. In your terminal, ensure your are in the projects base `capstone` directory and run the following commands. Please complete the prompts for the superuser:

	> `python manage.py makemigrations`
	>
	> `python manage.py migrate`
	>
	> `python manage.py createsuperuser`
	>
	> `python manage.py runserver`

Now in your web browser, access the application at `127.0.0.1:8000`. You should see a base map of the United States fill the webpage. If not, double check that your API keys are set up properly!  


### Step 4: Add Cities

Access the Django admin via `127.0.0.1:8000/admin`. Here we will add your desired cities to the `Cities` model. For purposes of this tutorial add the following entries:

	> Name: Austin
	> State: TX
	> Viewport lat: 30.258995
	> Viewport long: -97.746332
	>
	> Name: San Francisco
	> State: CA
	> Viewport lat: 37.783790
	> Viewport long: -122.398953

Afterwards, navigate back to the index page (`127.0.0.1:8000`)and you should be able to see both cities added to base map with pins. Clicking on the pin will create a popup with that city's name. Now click on the city name within the popup and the page will redirect you to a 3D map of that city. Toggling between cities is also now accessible via the dropdown menu at the top left corner of the map.  

### Step 5: Add permits

Next we will add the issued construction permits to our database for both of the defined cities.

In the terminal, stop the web application by typing `crtl + c`. Next, run the following two commands:

	> `python manage.py atx_permits`
	> `python manage.py sfo_permits`

After the commands have completed we can relaunch the application by typing `python manage.py runserver`.

Now when you navigate to either of the city's web pages, you should see it populated with pins at each permit location. Hovering over the pin will present a popup with that permit's name as defined by the city and clicking on the name will open a new tab with that permit's info on the city's website.

Congratulations, you have successfully completed the initial installation of the application. Next we will highlight featured construction projects in the city.  

### Step 6: Add building

In this step, we are going to identify a specific building that is under construction and aggregate the data into one entry. Via the Django Admin interface, go to the `Buildings` Model and click `Add Building`. For this tutorial enter the following attributes:

	> Name: Block 185
	> Img: "Block_185.jpg" (located in `capstone\city3d\static\city3d\buildings\Austin\img`)
	> Img Cred: Pelli Clarke Pelli, STG Design, Trammell Crow Company
	> Address: 601 W 2nd St
	> Developer: Trammell Crow Company
	> Contractor: DPR Construction
	> Architect: Pelli Clarke Pelli, STG Design,
	> Permit: 2020-071590 BP
	> City: Austin

Once saved, we will also need to link to this building via the appropriate permit model instance. Navigate to the Permits admin subfolder and search for `2020-071590 BP` as defined in the entry above. Now click on the `id` for that entry to edit that permit instance and select `Block 185` in the `Building` field.

Now when you navigate back to `127.0.0.1:8000/city/Austin`, the permit associated with the building will appear red. Hovering over the permit shows the building's name and clicking on the pin will display a sidebar containing all of that building's info. Feel free to pause here and check out the data included in this sidebar. You will notice that the news section at the bottom is empty. This brings us to our last step.  

### Step 7: Add headline

Navigate back to the Django admin interface and add a new `Headline`. For this tutorial, enter the following:

	> Datetime: 2021-07-22
	>	  			 14:13:30
	> Title: Block 185, Austin’s New ‘Google Tower,’ Officially Topped Out Downtown
	> Publisher: Towers.net
	> Link: https://austin.towers.net/block-185-austins-new-google-tower-officially-topped-out-downtown/
	> Img: https://austin.towers.net/wp-content/uploads/sites/19/block_185_topping_out_feature_1-2048x1408.jpg
	> Building: Block 185

Once saved, you can reload the website to `127.0.0.1:8000/city/Austin` and click on the red pin titled `Block 185`. The sidebar will pop up and you can now find the article featured within the `Recent News` section.

Congratulations, you've completed the set up and can now add as many permits, buildings, and news articles as you want to the web application.
