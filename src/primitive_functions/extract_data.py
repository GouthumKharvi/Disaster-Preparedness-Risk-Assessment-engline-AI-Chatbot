# primitive_functions/extract_data.py

def extract_data(obj, keys):
    """
    Primitive Function: extractData()
    
    Extracts only the specified keys from a dictionary-like object.
    
    Parameters:
        obj (dict): Input dictionary containing user data or structured information.
        keys (list): List of keys to extract.
    
    Returns:
        dict: A new dictionary containing only the requested keys.
    """
    if not isinstance(obj, dict):
        raise ValueError("extract_data expects obj to be a dictionary.")

    return {key: obj.get(key) for key in keys}
 
