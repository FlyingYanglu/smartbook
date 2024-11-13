import influxdb
from collections import defaultdict
import yaml
import json

class Data:
    def __init__(self, config_path="smartbook/configs/model_config.yaml"):
        """
        Initialize the Data object using parameters from a configuration file.
        """
        
        # Load configuration from the specified YAML file
        self.load_config(config_path)

        # Create a 2-dimensional map using defaultdict
        self.room_data = defaultdict(lambda: defaultdict(float))

    def load_config(self, config_path):

        # Load configuration from the specified YAML file
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Extract InfluxDB connection details from the configuration
        connection_config = config['DataFetcher']['ConnectionConfig']
        self.host = connection_config['HOST']
        self.port = connection_config['PORT']
        self.username = connection_config['USERNAME']
        self.password = connection_config['PASSWORD']
        self.database = connection_config['DATABASE']
        self.ssl = connection_config['SSL']

        # Initialize the InfluxDB client using config parameters
        self.client = influxdb.InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
            ssl=self.ssl,
            verify_ssl=True
        )

        # Extract query configuration details from the configuration
        query_config = config['DataFetcher']['QueryConfig']
        self.rooms = query_config['Rooms']
        self.measurements = query_config['Measurements']
        self.timespan = query_config['timespan']

    def query(self, room, measurement):
        """
        Query the InfluxDB for a specific room and measurement.
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
    
    
    def format_data(self, data):
        """
        Format self.room_data (a nested defaultdict) into a JSON string with a newline after each room's entry.
        """
        # Convert defaultdict to a regular dict for JSON serialization
        formatted_data = {room: dict(readings) for room, readings in data.items()}

        # Serialize the data with a newline after each room's entry
        json_lines = [f'"{room}": {json.dumps(readings, ensure_ascii=False)}' for room, readings in formatted_data.items()]
        return '{' + ',\n'.join(json_lines) + '}\n'
    
    
    def collect_data(self, formatter=None):
        """
        Collect data for all rooms and measurements, using format_data by default.
        """
        # If no formatter is provided, use the default format_data method
        if formatter is None:
            formatter = self.format_data

        # Collect data for each room and measurement
        for room in self.rooms:
            for measurement in self.measurements:
                self.query(room, measurement)
        
        # Format the data using the formatter
        return formatter(self.room_data)
    
    

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


# # Usage Example
# # Initialize the Data class with the path to the YAML configuration file
# config_path = 'path/to/your/config.yaml'
# lab_data = Data(config_path)

# # Collect and display data
# lab_data.collect_data()
# lab_data.display_data()
