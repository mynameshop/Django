from __future__ import unicode_literals
from django.db import models
from django.contrib.sites.models import Site
from tinymce.models import HTMLField
from apps.base.models import ModelCreatetAtMixin, ModelDatetimeMixin
from apps.billing.plan_template import PRICING_TEMPLATES_CHOICES, PRICING_TEMPLATES
import settings

def get_project_request_folder(instance, filename):
    return 'project_request/{0}/{1}'.format(instance.project_request_id, filename)

class SiteSettings(ModelDatetimeMixin):
    site = models.OneToOneField(Site)
    homepage_header_image = models.ImageField(upload_to="sitemedia")
    homepage_header_text_first = HTMLField(
        max_length=128,
        default='CONVERT YOUR ECOMMERCE STORE INTO A 3D EXPERIENCE'
    )
    homepage_header_text_second = HTMLField(
        max_length=256, 
        default='Give your customers an amazing buying experience! Easily implement with one line of code.'
    )
    homepage_header_text_button = models.CharField(max_length=256, default='sign up for offers')
    
    homepage_first_sample_label = models.CharField(max_length=64, default='Affordability')
    homepage_first_sample_text = HTMLField(
        default="\
            <p>A new experience within your budget.</p>\
            <p>Quality 3D models that won't break your bank Cost-efficient web hosting.</p>\
            <p>Compelling demos lead to increased revenue greater client satisfaction and tangible results.</p>"
    )
    homepage_second_sample_label = models.CharField(max_length=64, default='Your Product In 3D')
    homepage_second_sample_text = HTMLField( 
        default="\
            <p>What if you could demonstrate your product in a whole new way that will encourage your customers to buy?</p>\
            <ul>\
                <li>Give users a feel for your product before they buy.</li>\
                <li>Instantly call out product features.</li>\
                <li>Ignite your users creativity.</li>\
                <li>Spark your users genius.</li>\
            </ul>"
    )
    
    homepage_label_how_it_work = models.CharField(max_length=64, default='Stop Losing Customers - Start Engaging')
    homepage_text_how_it_work = HTMLField(
        default="Bringing attention to your product can be a real challenge, especially \
        if you only have a couple of simple images and a description. Stop telling them \
        about your product and start letting them experience it for themselves.<br />Don&rsquo;t \
        worry, implementing Canvas Gadget's 3D marketing content is as easy as adding a single line \
        of code to your website."
    )
    homepage_text_step_1 = models.CharField(max_length=64, default='Tell Us About Your Product')
    homepage_text_step_2 = models.CharField(max_length=64, default='Let us do all the work')
    homepage_text_step_3 = models.CharField(max_length=64, default='Publish the result with one line of code')
    
    # feedbackpage ======================
    feedbackpage_header_image = models.ImageField(upload_to="sitemedia", null=True, blank=True)
    feedbackpage_social_text = models.CharField(
        max_length=128,
        default='Drop Us A Line'
    )
    feedbackpage_form_text = HTMLField(
        default='Have a question or a comment?<br>Feel free to let us know.'
    )
    feedbackpage_message_label = models.CharField(max_length=128, default='Message')
    feedbackpage_message_text = HTMLField(
        default='Lorem ipsum dolor sit amet'
    )
    feedbackpage_submit_button_text = models.CharField(max_length=128, default='Send Message')
    # =====================================
    
    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"
        
class HomepageRowItem(ModelDatetimeMixin):
    sitesettings = models.ForeignKey(SiteSettings)
    image = models.ImageField(upload_to="sitemedia")
    label = models.CharField(max_length=128)
    text = HTMLField()
    
    class Meta:
        verbose_name = "home page row item"
        verbose_name_plural = "home page row items"

PROJECT_REQUEST_STATUS_NEW = 0
PROJECT_REQUEST_STATUS_ON_REVIEW = 1
PROJECT_REQUEST_STATUS_READY = 2
PROJECT_REQUEST_STATUS = (
    (PROJECT_REQUEST_STATUS_NEW, 'new'),
    (PROJECT_REQUEST_STATUS_ON_REVIEW, 'on review'),
    (PROJECT_REQUEST_STATUS_READY, 'ready'),
)
    
class ProjectRequest(ModelCreatetAtMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    project_name = models.CharField(max_length=128, null=False, blank=False)
    project_description = models.CharField(max_length=512, null=False, blank=False)
    subscription_template = models.IntegerField(choices=PRICING_TEMPLATES_CHOICES, default=1)
    
    status = models.SmallIntegerField(choices = PROJECT_REQUEST_STATUS, default=PROJECT_REQUEST_STATUS_NEW)
    
    def __str__(self):
        return self.project_name
    
    def get_email(self):
        return self.user.username if self.user else self.user_email
    
    def get_stripe_cost(self):
        tmpl = PRICING_TEMPLATES.get(self.get_subscription_template_display(), PRICING_TEMPLATES.get('silver'))
        cost = tmpl.get('subscription_cost', 10) * 100
        return cost
    
    def get_or_create_project(self):
        from apps.projects.models import Project
        try:
            self.project
        except Project.DoesNotExist:
            Project.objects.create(
                name = self.project_name, 
                description = self.project_description,
                owner = self.user,
                projectrequest = self,
            )
        return self.project
    
class ProjectRequestImage(ModelCreatetAtMixin):
    project_request = models.ForeignKey(ProjectRequest)
    image = models.ImageField(upload_to=get_project_request_folder)
    