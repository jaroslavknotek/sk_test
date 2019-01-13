# SpaceKnow API test

Aim of this project is to count cars on a given area for all available imagery for a given timespan.


Test data polygon in config is [Brisbane staff car parking, Brisbane Airport QLD 4008, Australia](https://www.google.com/maps/place/BNE+Staff+Carpark/@-27.3927375,153.103971,1237m/data=!3m1!1e3!4m8!1m2!2m1!1sbrisbane+airport+stuff+pariking+!3m4!1s0x6b915f54f339df27:0x6dfb50413ce64bad!8m2!3d-27.3905316!4d153.1047365)


## Requirements
- Pipenv to install all requirements with single command
- Python 3.6
- it requires SpaceKnow credentials id, username, password.

## Installation
~~~
pipenv install
~~~ 

And wait for it to download all necessary dependencies

## running

Script has following parameters 

~~~
--outputDir OUTPUTDIR
                        output directory
--config CONFIG
                        path to config file
~~~

Config looks like this
~~~json
{
	"credentials": {
		"id": "spaceknow_id",
		"user": "user_mail",
		"pass": "password"
	},
	"polygon": [[153.1050866, -27.3900761], [153.1042391, -27.3913812], [153.1035105, -27.3926031], [153.1045404, -27.393127], [153.1054202, -27.3935366], [153.1061819, -27.3921268], [153.1067389, -27.3908954], [153.1061381, -27.3905143], [153.1050866, -27.3900761]]
}
~~~
You can find it in `config/creds_sk.json`

### Example

~~~
pipenv run python src/main.py --outputDir output --config config\creds_sk.json
~~~

## Testing

go to `sk_test\src`

Enter command
~~~
python -m unittest
~~~


