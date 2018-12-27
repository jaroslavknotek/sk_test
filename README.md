# Test

The program should count cars for a staff parking lot for all available imagery.

Parking lot is represented by polygon inside main.py
All available imagery is vague term. Since scene api requires date span, the maximum span(observed on analytics.spaceknow.com) was used instead

## Requirements
- Pipenv to install all requirements with single command
- Python 3.6

## installation
locate `sk_test` directory
~~~
pipenv install
~~~ 

And wait for it to download all necessary dependencies

## running

Script has some parameters 

~~~
--outputDir OUTPUTDIR
                        output directory
--startDate STARTDATE
                        starting date of scene timeline
--endDate ENDDATE     
                        ending date of scene timeline
~~~

Example
~~~
pipenv run python src/main.py --outputDir output --startDate "2001-01-01 00:00:00" --endDate "2019-02-01 00:00:00"
~~~

## testing

go to `sk_test\src`

Enter command
~~~
python -m unittest
~~~


