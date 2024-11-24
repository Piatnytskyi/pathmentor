(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR
) = range(5)

ERRORS = {
    DIR_ERROR: "Directory error",
    FILE_ERROR: "File error",
    DB_READ_ERROR: "Database read error",
    DB_WRITE_ERROR: "Database write error"
}