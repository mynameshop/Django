# Create your tests here.
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from .forms import RegisterProfileForm

im = Image.new(mode='RGB', size=(200, 200))  # create a new image using PIL
im_io = BytesIO()  # a StringIO object for saving image
im.save(im_io, 'JPEG')  # save the image to im_io
im_io.seek(0)  # seek to the beginning

TestPhoto = InMemoryUploadedFile(
    im_io, None, 'random-name.jpg', 'image/jpeg', 10000, None
)


class UsernameTests(TestCase):
    form_data = {'email': 'example@example.com', "password": "QU!dIMhUuBN9t%Ik",
                 'display_name': "Test User", "birthday": '2/2/2010', "gender": 'm'}
    file_dict = {"avatar": TestPhoto}

    def test_invalid_user_names(self):
        invalid_user_list = ['Oba.ma', 'Obama-', 'O)bama', 'Ob ma']
        for user in invalid_user_list:
            self.form_data['username'] = user
            form = RegisterProfileForm(data=self.form_data, files=self.file_dict)
            self.assertTrue(not form.is_valid(), "RegisterProfileForm is  valid for user %s" % user)

    def test_valid_user_name(self):
        valid_user_list = ['Obama', 'HillaryClinton', 'riahana2535', 'Jonh15Doe']
        for user in valid_user_list:
            self.form_data['username'] = user
            form = RegisterProfileForm(data=self.form_data, files=self.file_dict)
            print(form.errors)
            self.assertTrue(form.is_valid(), "RegisterProfileForm is not valid for user %s" % user)
