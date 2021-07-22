## Details

Sensors in each spot that are linked to the entry in the RTDB. When the sensor is triggered on, update the RTDB. 

When the user selects the spot, update that in RTDB. 

Only the spots that have users linked to the spot will be able to provide prediction information about when the spot will become available. 

## Database Model For The Garage
{
    'cottage_grove'
        'floor #'
            'spots'
                '1'
                    'type'
                    'status'
                    'taken_by'
}