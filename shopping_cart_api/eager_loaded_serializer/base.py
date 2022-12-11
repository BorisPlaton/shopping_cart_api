class EagerLoadedSerializer:
    """
    The base class for populating instance for serializing
    with db data.
    """

    def __init__(self, instance=None, *args, eager_loading=False, **kwargs):
        if eager_loading and instance is not None:
            instance = self.setup_eager_loading(instance)
        super().__init__(instance, *args, **kwargs)

    def setup_eager_loading(self, model):
        """
        This method is called when the model is populated with data. It must
        return `instance` argument.
        """
        raise NotImplementedError(
            "You haven't implemented the `setup_eager_loading` method for populating a model."
        )
