from rest_framework import serializers
from .models import User, LedgerItem
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
    
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format")
        
        existing_users = User.objects.all()
        for user in existing_users:
            if user.email == value:
                raise serializers.ValidationError("Email already exists")
        
        return value
    
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")
        return value
    
    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError("Invalid credentials")
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")
            
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include email and password")
        
        return data


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'date_joined', 'is_active']
    
    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    ledger_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'date_joined', 'is_active', 'ledger_count']
    
    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name
    
    def get_ledger_count(self, obj):
        count = 0
        for item in LedgerItem.objects.all():
            if item.author.id == obj.id:
                count = count + 1
        return count


class LedgerItemCreateSerializer(serializers.ModelSerializer):
    contents = serializers.CharField(max_length=1000)
    
    class Meta:
        model = LedgerItem
        fields = ['contents']
    
    def validate_contents(self, value):
        if value == "":
            raise serializers.ValidationError("Contents cannot be empty")
        if len(value) == 0:
            raise serializers.ValidationError("Contents must have text")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        ledger_item = LedgerItem()
        ledger_item.author = user
        ledger_item.contents = validated_data.get('contents')
        ledger_item.save()
        
        return ledger_item


class LedgerItemListSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    
    class Meta:
        model = LedgerItem
        fields = ['item_id', 'author_email', 'author_name', 'contents', 'preview', 'created_datetime']
    
    def get_author_email(self, obj):
        return obj.author.email
    
    def get_author_name(self, obj):
        return obj.author.first_name + " " + obj.author.last_name
    
    def get_preview(self, obj):
        if len(obj.contents) > 50:
            preview = ""
            for i in range(50):
                preview = preview + obj.contents[i]
            return preview + "..."
        else:
            return obj.contents


class LedgerItemDetailSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = LedgerItem
        fields = ['item_id', 'author_email', 'author_name', 'author_id', 'contents', 'created_datetime', 'formatted_date']
    
    def get_author_email(self, obj):
        return obj.author.email
    
    def get_author_name(self, obj):
        return obj.author.first_name + " " + obj.author.last_name
    
    def get_author_id(self, obj):
        return obj.author.id
    
    def get_formatted_date(self, obj):
        date = obj.created_datetime
        return str(date.year) + "-" + str(date.month) + "-" + str(date.day) + " " + str(date.hour) + ":" + str(date.minute)