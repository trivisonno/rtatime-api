# RTA-TIME API

Allows a user to search a transit stop number for the next arriving transit vehicles. Useful with the Greater Cleveland Regional Transit Authority (GCRTA). Relies entirely on data provided by the GCRTA NextConnect real-time vehicle location system. Real-time arrival information may not always be precise, and all data issues should be referred to GCRTA.

## Description

GCRTA relies on [NextConnect software](http://nextconnect.riderta.com/) to track transit vehicle locations and predicted arrival times at all transit stops. GCRTA provides access to this information [on its website](http://nextconnect.riderta.com/LiveDepartureTimes), where users can search for next arriving vehicles, but only with limited search criteria. There presently is no method to search by Stop Name or 5-digit Stop #.

This API merges data from the agency's GTFS and NextConnect systems to allow for easy search-by-stop in a way not otherwise available to users. The three supporting json/geojson files are required to tied together the two GTFS and NexctConnect systems. With this app, you can build all sorts of real-time arrival programs or displays.

For example, this API is presently used for a real-time SMS text-based system for riders without data plans or smartphones using Twilio virtual phone numbers. This app uses the JSON data to construct a useful text message for riders. If a rider sends the below 5-digit Stop # (often displayed on the signs) to the virtual number,
```
03457
```
the following text message is returned
```
DETROIT AV & W 65TH ST
26: 1131a, 1147a
26A: 1117a
```

## Getting Started

Ensure that you have Python 3 installed on your system. I recommend using pipenv for testing.

### Dependencies

* Python 3.8, Flask

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders
```
$ git clone https://www.github.com/trivisonno/rtatime-api
$ cd rtatime-api
$ pipenv shell --python 3.8
$ pip install flask
```

To test locally:
```
export FLASK_APP=api.py
flask run
```

If you have an AWS account set up and wish to deploy to AWS Lambda for use in apps, then deploy with zappa:
```
$ pip install zappa
$ zappa init
$ zappa deploy dev
```

### Executing program

If running locally with Flask, then add the 5-digit Stop # as below (Stop # 03457 as example)
```
http://127.0.0.1:5000/03457
```

If deployed to the AWS API Gateway with Lambda, make a GET request to
```
https://abc1234.execute-api.us-east-1.amazonaws.com/dev/03457
```

Both will return a JSON response that includes an array of routes with arrival times
```
{"arrivals":[{"d":{"errorMessage":null,"routeStops":[{"routeID":165,"stops":[{"alerts":null,"crossings":[{"cancelled":false,"countdown":null,"destination":"26A Detroit to Downtown","predPeriod":"pm","predTime":"8:39","schedPeriod":"pm","schedTime":"8:18"},{"cancelled":false,"countdown":null,"destination":"26 Public Square","predPeriod":"pm","predTime":"8:51","schedPeriod":"pm","schedTime":"8:48"},{"cancelled":false,"countdown":null,"destination":"26A Detroit to Downtown","predPeriod":"pm","predTime":"9:18","schedPeriod":"pm","schedTime":"9:18"}],"directionID":3,"sameDestination":false,"stopID":9194,"timePointID":0}]}],"showArrivals":false,"showDestination":true,"showScheduled":true,"showStopNumber":false,"updatePeriod":"pm","updateTime":"8:24"}}],"request":"03457","stopName":"DETROIT AV & W 65TH ST"}
```


## Authors

Angelo [@Trivisonno](https://twitter.com/Trivisonno)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Unlicense (Public Domain)- see the LICENSE file for details
