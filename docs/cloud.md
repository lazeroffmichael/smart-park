## Real Time Database
The Real Time Database (RTDB) will be used to contain the garage state and update the state to all the users.

## Firestore Database
The firestore database will be used to hold other information (such as user information, coordinate information etc)

## ML Pipeline
- Receive GPS coords
- Receive ID of the user
1) Determine if coords inside of geofence
2) If inside, make the prediction for whether or not the person is returning to the garage.
3) If prediction is true, then make the time estimation for the spot and update the field in the RTDB. 

### How Works
Have a main function which will make the calls for all the sub functions to be ran. 

ex.

```python
def main(coords, user_id):
    # Determine if coords are in the geofence
    check_geofence()
    
    # If coords are in geofence make prediction
    prediction()

    # If prediction is true update the prediction time in the DB
    predict_time()
```
## IoT Devices

- Parking sensors are simulated and communicate through http requests. In a real life scenario, devices can also communicate with MQTT. The role of the devices is to update the state of the RTDB. To manage the IoT devices, Google IoT core could be used and configured to do the necessary updates. 

## Geofence
A geofence is used to define the region around the parking garage where user trajectory can be reasonably predicted. 
This geofence could be adapted to extend to a farther range if there are specific pathways where it is likely that 
individuals headed a certain direction are returning to the parking garage.

## Determining If A User Is Inside Of The Geofence
Since the geofence is a defined set of coordinates, we can determine whether or not a user's GPS coordinates are 
inside of the geofence by using an algorithm that determines whether a point is contained inside of a polygon. 

