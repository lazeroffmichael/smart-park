## Geofence
A geofence is used to define the region around the parking garage where user trajectory can be reasonably predicted. 
This geofence could be adapted to extend to a farther range if there are specific pathways where it is likely that 
individuals headed a certain direction are returning to the parking garage.

## Determining If A User Is Inside Of The Geofence
Since the geofence is a defined set of coordinates, we can determine whether or not a user's GPS coordinates are 
inside of the geofence by using an algorithm that determines whether a point is contained inside of a polygon. 