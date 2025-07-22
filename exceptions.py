class ProfileNameAlreadyExistsError(Exception):
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        super().__init__(f"A profile with the name '{profile_name}' already exists.")


class ProfileLimitReachedError(Exception):
    def __init__(self, model_name: str, limit: int):
        self.model_name = model_name
        self.limit = limit
        super().__init__(f"Profile limit of {limit} reached for model {model_name}")
