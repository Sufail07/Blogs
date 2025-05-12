from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Post
# Create your tests here.


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='secret',
            email='test@gmail.com'
        )
        
        self.post = Post.objects.create(
            title='A good title',
            author=self.user,
            body="nice body content"
        )
        
    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'nice body content')
        
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'nice body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1')
        no_response = self.client.get('/post/10000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': "New Title",
            'author': self.user,
            'body': "New text",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Title")
        self.assertContains(response, 'New text')
        
    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': "Updated title",
            'body': "Updated content",
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse("post_delete", args='1'))
        self.assertEqual(response.status_code, 200)

        
        