
import pickle


def load_db_schema(schema_file):
    """
    Loads the database schema from a file using pickle and prints it formatted for user-friendly display.

    Parameters:
    schema_file (str): Path to the file where the schema is saved.
    """
    try:
        with open(schema_file, "rb") as f:
            schema_definitions = pickle.load(f)

            # Print introduction
            print("[bold magenta]Database Schema Overview[/bold magenta]\n")

            # Print each schema definition with description
            for definition in schema_definitions:
                if definition:
                    table_name = definition.split('(')[0]
                    schema_text = f"[bold cyan]Table Name:[/bold cyan] {table_name}\n{definition}"
                    print(f"[bold]{schema_text}[/bold]\n")

    except FileNotFoundError:
        print(f"Error: File '{schema_file}' not found.")
    except IOError as e:
        print(f"Error: IOError occurred while reading '{schema_file}': {e}")

if __name__ == "__main__":
    schema_file = "../schemas/northwind_schema.pkl"
    load_db_schema(schema_file)
