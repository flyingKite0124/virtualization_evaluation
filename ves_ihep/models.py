from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.


class Scene(models.Model):
    name = models.CharField(max_length=128, unique=True)
    stable = models.BooleanField(default=False)
    slug = models.SlugField(default='', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Scene, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

"""class Script(models.Model):
	scenen = models.ManyToManyField(Scene)
	name = models.CharField(max_length=128, unique=True)
	script = models.FileField(upload_to='scripts/%Y/%m/%d')

	def __unicode__(self):
		return self.name	"""


class Script(models.Model):
    script_name = models.CharField(max_length=120)
    upload_time = models.DateTimeField()
    script_type = models.CharField(max_length=30)
    script_path = models.CharField(max_length=240,null=True)

    def __unicode__(self):
        return self.script_name


class Host(models.Model):
    IP = models.GenericIPAddressField()
    username = models.CharField(max_length=128)
    passwd = models.CharField(max_length=128)
    status = models.IntegerField(default=0)
    alias = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.IP


class Activity(models.Model):
    activity_name = models.CharField(max_length=30)
    script = models.ForeignKey(Script)
    scene = models.ForeignKey(Scene)

    def __unicode__(self):
        return self.activity_name


class SceneHistory(models.Model):
    scene = models.ForeignKey(Scene)


class ActivityHistory(models.Model):
    stdout_path = models.CharField(max_length=240, null=True)
    stderr_path = models.CharField(max_length=240, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)
    host = models.ForeignKey(Host)
    activity = models.ForeignKey(Activity)
    scene_history = models.ForeignKey(SceneHistory)
