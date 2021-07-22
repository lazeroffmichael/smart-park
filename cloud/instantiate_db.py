"""
Populates the Real Time Database with the initial state of the garage. The initial state of the garage has all the
the spots open.
"""
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Constants for the type of spot
STAFF = "staff"
HANDICAPPED = "handicapped"
STANDARD = "standard"
RESERVED = "reserved"
COMPACT = "compact"
ELECTRIC_VEHICLE = "electric_vehicle"


def update(start: int,
           end: int,
           parent_ref: str,
           type: str or dict,
           compact: bool=False,
           metered: bool=False,
           status: str='open',
           occupied_by: str='none',
           electric_vehicle: bool=False):
    """
    Creates new entries in the database for the spots in the given range. All the spots will be updated with the same
    fields.

    Args:

        start: Starting ID of the spots to set
        end: Ending ID of the spots to set
        parent_ref: The path of the parent node that the new spots should be included under
        type: The type of the parking spot
            options = {'reserved', 'handicapped', 'standard', 'staff'}
        compact: Boolean for if the spot is compact
        metered: Boolean for if the spot is metered
        status: The status of the parking spot
            options = {'occupied', 'open'}
        occupied_by: The id of the parking spot
            options = {'{actual user id}', 'none'}
        electric_vehicle: Whether the spot supports electric vehicles
    Returns: None
    """
    data = {}
    for i in range(start, end + 1):
        # Add the entry to the data with the spot number as the index
        data[f'{i}'] = {
            'type': type,
            'compact': compact,
            'metered': metered,
            'status': status,
            'occupied_by': occupied_by,
            'electric_vehicle': electric_vehicle
        }
    # Actually update the database
    parent_ref.update(data)


# Fetch the service account key JSON file
cred = credentials.Certificate(os.getenv('ADMIN_PATH'))

# Initialize the app
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('databaseURL')
})

# Populate the amount of spots for floor 1
ref = db.reference('cottage_grove/floor_1')
ref.set({
    'total_spots': 315
})

# Set the new parent ref
ref = ref.child('spots')

# spots 1 - 3 which are Non-metered staff spots
update(1, 3, ref, STAFF)

# spots 4-11 which are metered, handicapped spots
update(4, 11, ref, HANDICAPPED, metered=True)

# spots 12-17 which are reserved, compact spots
update(12, 17, ref, RESERVED, compact=True)

# spots 18-23 which are metered, handicapped spots
update(18, 23, ref, HANDICAPPED, metered=True)

# spots 24-56 are standard, metered spots
update(24, 56, ref, STANDARD, metered=True)

# spots 57-86 are staff spots
update(57, 86, ref, STAFF)

# spots 87-90 are reserved
update(87, 90, ref, RESERVED)

# spots 91-124 are staff spots
update(91, 124, ref, STAFF)

# spots 125-136 are staff spots
update(125, 136, ref, STAFF)

# spots 137-178 are reserved spots
update(137, 178, ref, RESERVED)

# spots 179-191 are staff spots
update(179, 191, ref, STAFF)

# spots 192-224 are reserved spots
update(192, 224, ref, RESERVED)

# spot 225 is a staff, compact spot
update(225, 225, ref, STAFF, compact=True)

# spot 226-253 are staff spots
update(226, 254, ref, STAFF)

# spot 254 is a staff, compact spot
update(254, 254, ref, STAFF, compact=True)

# spots 255-281 are staff, compact spots
update(255, 281, ref, STAFF, compact=True)

# spots 282-296 are staff
update(282, 296, ref, STAFF)

# spots 297-300 are staff, electric vehicle spots
update(297, 300, ref, STAFF, electric_vehicle=True)

# spots 301-314 are staff
update(301, 314, ref, STAFF)

# spot 315 is staff and compact
update(315, 315, ref, STAFF, compact=True)