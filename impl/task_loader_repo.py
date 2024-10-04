from domain.config.loader import AbstractTaskLoaderRepository, AbstractTaskLoader


class TaskLoaderRepository(AbstractTaskLoaderRepository):
    LOADERS: list[AbstractTaskLoader] = []

    def get_task_loader(self, loader_name: str) -> AbstractTaskLoader | None:
        for loader in self.LOADERS:
            if loader.name == loader_name:
                return loader
        return None
