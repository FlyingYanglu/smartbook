# import aioinflux  # Asynchronous InfluxDB client
# from collections import defaultdict
# import aiofiles  # For asynchronous file operations
# import yaml
# import json
# import asyncio
# import time


# class Data_async:
#     def __init__(self, config_path="smartbook/configs/model_config.yaml"):
#         """
#         Initialize the Data object using parameters from a configuration file.
#         """
#         self.room_data = defaultdict(lambda: defaultdict(float))
#         # Load configuration from the specified YAML file asynchronously
#         asyncio.run(self.load_config(config_path))

#     async def load_measurements_config(self, measurements_config_path):
#         async with aiofiles.open(measurements_config_path, 'r', encoding="utf-8") as file:
#             content = await file.read()
#         measurements_config = yaml.safe_load(content)
#         self.measurements = measurements_config['metrics']

#     async def load_config(self, config_path):
#         # Load configuration from the specified YAML file asynchronously
#         async with aiofiles.open(config_path, 'r') as file:
#             content = await file.read()
#         config = yaml.safe_load(content)

#         # Extract InfluxDB connection details from the configuration
#         connection_config = config['DataFetcher']['ConnectionConfig']
#         self.host = connection_config['HOST']
#         self.port = connection_config['PORT']
#         self.username = connection_config['USERNAME']
#         self.password = connection_config['PASSWORD']
#         self.database = connection_config['DATABASE']
#         self.ssl = connection_config['SSL']

#         # Initialize the asynchronous InfluxDB client
#         self.client = aioinflux.InfluxDBClient(
#             host=self.host,
#             port=self.port,
#             username=self.username,
#             password=self.password,
#             db=self.database,
#             ssl=self.ssl,
#             mode='async'
#         )

#         # Extract query configuration details from the configuration
#         query_config = config['DataFetcher']['QueryConfig']
#         self.rooms = query_config['Rooms']
#         self.timespan = query_config['timespan']
#         self.num_decimals = query_config['num_decimals']
#         await self.load_measurements_config(query_config['measurements_config_path'])

#     async def query(self, room, measurement):
#         """
#         Query the InfluxDB for a specific room and measurement asynchronously.
#         """
#         query = (
#             f'SELECT mean(value) FROM "{measurement}" '
#             f'WHERE time > now() - {self.timespan} AND "location_specific" = \'{room}\' '
#             f'GROUP BY time(1m);'
#         )
#         result = await self.client.query(query)

#         val = 0
#         cnt = 0
#         for k, v in result.items():
#             for d in v:
#                 if 'mean' in d and d['mean'] is not None:
#                     val += d['mean']
#                     cnt += 1

#         # Store the result in the room_data dictionary
#         if cnt > 0:
#             avg = val / cnt
#             avg = round(avg, self.num_decimals)
#             self.room_data[room][measurement] = avg
#         else:
#             self.room_data[room][measurement] = None

#     def format_data(self, data):
#         """
#         Format self.room_data (a nested defaultdict) into a JSON string with a newline after each room's entry.
#         """
#         formatted_data = {room: dict(readings) for room, readings in data.items()}
#         json_lines = [f'"{room}": {json.dumps(readings, ensure_ascii=False)}' for room, readings in formatted_data.items()]
#         return '{' + ',\n'.join(json_lines) + '}\n'

#     async def collect_data(self, formatter=None):
#         """
#         Collect data for all rooms and measurements asynchronously, using format_data by default.
#         """
#         tasks = []
#         for room in self.rooms:
#             for measurement in self.measurements:
#                 tasks.append(self.query(room, measurement))

#         # Run all queries concurrently
#         await asyncio.gather(*tasks)

#         # Return the formatted data
#         return self.return_data(formatter)

#     def return_data(self, formatter=None):
#         """
#         Return the collected data in the desired format.
#         """
#         if formatter is None:
#             formatter = self.format_data

#         formatted_data = formatter(self.room_data)

#         # Add current time to the data
#         cur_time = "Current Time: " + time.strftime('%H:%M:%S')
#         formatted_data = cur_time + "\n" + formatted_data
#         return formatted_data

#     def display_data(self):
#         """Display the collected data."""
#         print(self.room_data)
#         for room, readings in self.room_data.items():
#             print(f"Room: {room}")
#             for metric, value in readings.items():
#                 if value is not None:
#                     print(f"  {metric}: {value:.2f}")
#                 else:
#                     print(f"  {metric}: No data")
#             print("-" * 30)
