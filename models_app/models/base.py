from django.db import models

class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		abstract = True



class SoftDeleteManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(is_deleted=False)


class BaseSoftDeleteModel(BaseModel):
	is_deleted = models.BooleanField(default=False)

	objects = SoftDeleteManager()

	def soft_delete(self):
		if self.is_deleted == False:
			self.is_deleted = True
			self.save(update_fields=["is_deleted"])

	def restore(self):
		if self.is_deleted:
			self.is_deleted = False
			self.save(update_fields=["is_deleted"])

	class Meta:
		abstract = True
