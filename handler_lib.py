"""Library for Handler functions and Stats for database *commands*"""

def parse_message(data: str):
    """Return a tuple containing the command, the key, and (optionally) the
    value cast to the appropriate type."""
    command, key, value, value_type = data.strip().split(';')
    if value_type:
        if value_type == "LIST":
            value = value.split(",")
        elif value_type == "INT":
            value = int(value)
        else:
            value = str(value)
    else:
        value = None
    return command, key, value


def update_stats( command: str, success: bool, stats: dict ):
    """Update stats dict with info about if executing command was a success"""
    if success:
        stats[command]["success"] += 1
    else:
        stats[command]["error"] += 1


def handle_stats( stats: dict ):
    """Return a tuple containing True and the contents of STATS dict"""
    return ( True, str( stats ) )


def handle_put( key, value, data: dict ):
    """Return a tuple containing True and the message to send back to the client"""
    data[key] = value
    return ( True, f"Key [{key}] set to [{value}]" )


def handle_get( key, data: dict ):
    """Return a tuple containing True if the key exists and the message to send back to the client."""
    if key not in data:
        return( False, f"ERROR: Key [{key}] not found" )
    else:
        return( True, data[key] )


def handle_putlist( key, value, data: dict ):
    """Return a tuple containing True if the command succeeded and the message to send back to the client"""
    return handle_put( key, value, data )


def handle_getlist( key, data: dict ):
    """Return a tuple containing True if the key contained a list and the message to send back to the client."""
    exists, value = handle_get(key, data)
    return_value = exists, value

    if not exists:
        return return_value
    
    elif not isinstance( value, list):
        return ( False, f"ERROR: Key [{key}] contains non-list value ([{value}])" )
    
    else:
        data[key] = value + 1
        return ( True, f"Key [{key}] incremented" )
    

def handle_increment(key, data):
    """Return a tuple containing True if the key's value could be incremented
    and the message to send back to the client."""
    exists, value = handle_get(key, data)
    return_value = exists, value

    if not exists:
        return return_value

    elif not isinstance(value, int):
        return ( False, f"ERROR: Key [{key}] contains non-int value ([{value}])" )

    else:
        data[key] = value + 1
        return ( True, f"Key [{key}] incremented" )


def handle_append(key, value, data: dict):
    """Return a tuple containing True if the key's value could be appended to 
    and the message to send back to the client"""
    exists, list_value = handle_get(key, data)
    return_value = exists, value

    if not exists:
        return return_value

    elif not isinstance( list_value, list ):
        return ( False, f"ERROR: Key [{key}] had value [{value}] appended" )

    else:
        data[key].append( value )
        return ( True, f"Key [{key}] had value [{value}] appended" )


def handle_delete(key, data: dict):
    """Return a tuple containing True if the key could be deleted and the 
    message to send back to the client."""
    if key not in data:
        return ( False, f"ERROR: Key [{key}] not found and could not be deleted")
    else:
        del data[key]
