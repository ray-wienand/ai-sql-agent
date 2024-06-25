import pickle

def get_schema(schema_file):
  try:
    with open(schema_file, 'rb') as file:
      schema_definitions = pickle.load(file)
      print(f" Schema file opened.")

      return schema_definitions

  except FileNotFoundError:
    print(f"Error: {schema_file} not found.")
    return None
  except IOError as e:
    print(f"Error: IOError occurred while reading the {schema_file}: e")
    return None


if __name__ == '__main__':
  schema_file = './schemas/northwind_schema.pkl'
  schema = get_schema(schema_file)
  