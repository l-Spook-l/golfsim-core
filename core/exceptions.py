class ProfileNameAlreadyExistsError(Exception):
    """Raised when trying to create a profile with a name that already exists."""

    def __str__(self):
        return "A profile with this name already exists"


class ProfileLimitReachedError(Exception):
    """Raised when the user has reached the maximum allowed number of profiles."""

    def __str__(self):
        return "You’ve reached the maximum number of profiles"
