from django.db import models
from models_app.models import *


class DataMixin:
	is_deleted = models.BooleanField(default=False)

	def soft_delete(self):
		if is_deleted == False:
			self.is_deleted = True
			self.save()

	def get_revert(self):
		if is_deleted:
			self.is_deleted = False
			self.save()

	class Meta:
		abstract = True
		