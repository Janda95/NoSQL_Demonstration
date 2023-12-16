# NoSQL_Demonstration
An example of the inner workings and operations of a NoSQL database as a standalone server.


**NOTE:**
Work in progress example used a playground for building and understanding the fundamentals behind NoSQL database operations throught simple implementation.


### Structure for Request Messages
COMMAND;[KEY];[VALUE];[VALUE TYPE]

    COMMAND is a command from the list above

    KEY is a string to be used as a data store key (optional)

    VALUE is a integer, list, or string to be stored in the data store (optional)
        Lists are represented as a comma-separated series of strings, e.g. "red,green,blue"

    VALUE TYPE describes what type VALUE should be interpreted as
        Possible values: INT, STRING, LIST

Examples:


    "PUT;foo;1;INT"

    "GET;foo;;"

    "PUTLIST;bar;a,b,c;LIST"

    "APPEND;bar;d;STRING

    "GETLIST;bar;;"

    "STATS;;;"

    "INCREMENT;foo;;"

    "DELETE;foo;;"

