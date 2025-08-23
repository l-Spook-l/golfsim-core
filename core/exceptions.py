class ProfileNameAlreadyExistsError(Exception):
    def __str__(self):
        return "A profile with this name already exists"


class ProfileLimitReachedError(Exception):
    def __str__(self):
        return "You’ve reached the maximum number of profiles"
