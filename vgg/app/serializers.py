from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *








class AccountSignUpSeralizer(serializers.ModelSerializer):
    password_2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    interests = serializers.ListField(child=serializers.CharField(max_length=20))
    bio = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'username', 'password', 'password_2', 'email', 'interests', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        for i in ['first_name', 'last_name',  'username', 'password', 'password_2', 'email', 'interests', 'bio']:
            if i not in self.validated_data:
                raise serializers.ValidationError({i: f"{i} is needed"})
                
        password = self.validated_data['password']
        password_2 = self.validated_data['password_2']

        if password != password_2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        else:
            user = User(username=self.validated_data['username'], email=self.validated_data['email'])
            user.set_password(password)
            user.save()

            new_account = Account()
            
            new_account.user = user
            new_account.first_name = self.validated_data['first_name']
            new_account.last_name = self.validated_data['last_name']
            for role in self.validated_data['interests']:
                new_account.interests.append(role)
            new_account.bio = self.validated_data['bio']

            new_account.courses = []
            new_account.expert = False


            new_account.save()
            
            return new_account




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'interests', 'bio', 'created_at', 'expert', 'courses'] 



# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['name', 'email', 'organization', 'date_created']



# class ProfileUsername(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']


# class ProfileEmail(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['email']


# class ProfileName(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['name']


# #others

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()



class CourseCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['name', 'category']

    def save(self, request):
        for i in ['name', 'category']:
            if i not in self.validated_data:
                raise serializers.ValidationError({i: f"{i} is needed"})

        new_course = Course()
        new_course.name = self.validated_data['name']
        new_course.category = self.validated_data['category']
        new_course.created_by = request.user.username

        new_course.save()

        return new_course




class TestCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['name', 'questions', 'answers', 'category']

    def save(self, request):
        new_test = Test()

        new_test.creator = request.user.username
        new_test.name = self.validated_data['name']
        new_test.category = self.validated_data['category']

        for que in self.validated_data['questions']:
            new_test.questions.appqnd(que)

        for ans in self.validated_data['answers']:
            new_test.answers.append(ans)

        new_test.save()

        return new_test



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']




class AskQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question']


    def save(self, request):
        new_question = Question()

        new_question.question = self.validated_data['question']
        new_question.answers = []
        new_question.asked_by = request.user.username

        new_question.save()

        return new_question



class CreateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['name', 'category']


    def save(self, request):
        new_course = Course()

        new_course.name = self.validated_data['name']
        new_course.category = self.validated_data['category']
        new_course.created_by = Account.objects.get(user=request.user)


        new_course.save()

        return new_course


class CreateTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['name', 'questions', 'answers', 'category']


    def save(self, request):
        new_test = Test()

        new_test.name = self.validated_data['name']
        new_test.questions = [que for que in self.validated_data['questions']]
        new_test.answers = [ans for ans in self.validated_data['answers']]
        new_test.category = self.validated_data['category']

        new_test.creator = Account.objects.get(user=request.user)

        new_test.save()

        return new_test




class ExpertSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model= Expert_support
        fields= ["category", "question_text"]


    def save(self, request):
        new_support = Expert_support()

        new_support.question_text = self.validated_data['question_text']
        new_support.category = self.validated_data['category']
        new_support.user_email = request.user.email

        new_support.save()

        return new_support
