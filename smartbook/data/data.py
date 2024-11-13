import influxdb
from collections import defaultdict

class Lab_Data:

    def __init__(self, rooms, measurements, timespan='5m'): 
        """
        Initialize the Lab_Data object with InfluxDB connection
        and setup for querying rooms and measurements.
        """
        # InfluxDB connection details
        HOST = 'influx.linklab.virginia.edu'
        PORT = 443
        USERNAME = 'sahbf24'
        PASSWORD = 'raighee7Ahpheej3eud2sheob7seey7'
        DATABASE = 'gateway-generic'
        
        # Initialize the InfluxDB client
        self.client = influxdb.InfluxDBClient(
            HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True
        )
        
        # Store the rooms and measurements
        self.rooms = rooms
        self.measurements = measurements
        self.timespan = timespan
        
        # Create a 2-dimensional map using defaultdict
        self.room_data = defaultdict(lambda: defaultdict(float))

    def query(self, room, measurement):
        """
        Query the InfluxDB for a specific room and measurement
        """
        query = (
            f'SELECT mean(value) FROM "{measurement}" '
            f'WHERE time > now() - {self.timespan} AND "location_specific" = \'{room}\' '
            f'GROUP BY time(1m);'
        )
        result = self.client.query(query)

        val = 0
        cnt = 0
        for k, v in result.items():
            for d in v:
                if 'mean' in d and d['mean'] is not None:
                    val += d['mean']
                    cnt += 1

        # Store the result in the room_data dictionary
        if cnt > 0:
            avg = val / cnt
            self.room_data[room][measurement] = avg
        else:
            self.room_data[room][measurement] = None

    def collect_data(self):
        """
        Collect data for all rooms and measurements
        """
        for room in self.rooms:
            for measurement in self.measurements:
                self.query(room, measurement)

        return self.room_data

    def display_data(self):
        """Display the collected data."""
        print(self.room_data)
        for room, readings in self.room_data.items():
            print(f"Room: {room}")
            for metric, value in readings.items():
                if value is not None:
                    print(f"  {metric}: {value:.2f}")
                else:
                    print(f"  {metric}: No data")
            print("-" * 30)


'''
# List of rooms and measurements to query
rooms = ['211 Olsson', '217 Olsson', '225 Olsson', '251 Olsson', '204 Olsson']
measurements = ['Temperature_°C', 'co2_ppm', 'Illumination_lx']

# Initialize the Lab_Data class with rooms and measurements
lab_data = Lab_Data(rooms, measurements, '1d')

# Collect data for all specified rooms and measurements, return a 2d dict
lab_data.collect_data()

# Display the collected data
lab_data.display_data()
'''