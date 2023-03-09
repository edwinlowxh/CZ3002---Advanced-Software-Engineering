from django.db import models

class CarManager(models.Manager):
    def get_car(self, id: int) -> models.QuerySet:
        return self.filter(id=id)

    def get_unique_makes(self) -> models.QuerySet:
        return self.values_list('make', flat=True).distinct()

    def get_unique_models(self, make: str) -> models.QuerySet:
        return self.filter(make=make).values_list('model', flat=True).distinct()

    def get_model_spec(self, make: str, model: str) -> models.QuerySet:
        return self.filter(make = make, model = model).values_list('spec', flat=True).distinct()

    def search(self, search: str, limit: float) -> models.QuerySet:
        
        return self.get_queryset().filter(
            (models.Q(make__icontains=search) |
            models.Q(model__icontains=search) |
            models.Q(spec__icontains=search)) &
            models.Q(installment__lte=limit)
        )

                

        
        
