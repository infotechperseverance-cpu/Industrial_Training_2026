from pathlib import Path
#it is optional but you use you no show error
#this provide true path for anywhere required path 
def path_converter(path):
    try:
        # Check None
        if path is None:
            raise ValueError("Path cannot be None")

        # Check datatype
        if not isinstance(path, str):
            raise TypeError("Path must be string")

        # Remove spaces
        path = path.strip()

        # Check empty string
        if path == "":
            raise ValueError("Path cannot be empty")

        # Normalize slashes
        path = path.replace("\\", "/")

        # Remove duplicate slashes
        while "//" in path:
            path = path.replace("//", "/")

        # Convert to Path object
        converted_path = Path(path).as_posix()

        return converted_path

    except ValueError as e:
        print("Validation Error:", e)
        return None

    except TypeError as e:
        print("Type Error:", e)
        return None

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        return None

    except Exception as e:
        print("Unexpected Error:", e)
        return None