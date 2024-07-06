from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import EntryCategory, Entry
from entry.helpers.filter_helpers import FilterHelper
from user.models import UserModel

@api_view(['POST'])
def create_journal_category(request):
    response = Response()
    data = get_request_data(request)
    requesting_user = token_is_valid(data.get('token'))
    if requesting_user and data.get('category_name'):
        try:
            category_instance = EntryCategory.objects.create(
                category_name = data.get('category_name').lower()
            )
            response.status_code = 200
            response.data = {'cat_id': category_instance.category_uuid}
        except:
            response.status_code = 500
            response.data = {'status': 'ERROR'}
    else:
        response.status_code = 403
        response.data = {'status': 'NOT_ALLOWED'}
    return response

@api_view(['POST'])
def get_available_journal_categories(request):
    response = Response()
    data = get_request_data(request)
    requesting_user = token_is_valid(data.get('token'))
    if requesting_user:
        try:
            categories = [
                {
                    'name': category.category_name,
                    'uuid': category.category_uuid
                } for category in EntryCategory.objects.all()
            ]
            response.status_code = 200
            response.data = {'categories': categories}
        except:
            response.status_code = 500
            response.data = {'status': 'ERROR'}
    else:
        response.status_code = 403
        response.data = {'status': 'NOT_ALLOWED'}
    return response

@api_view(['POST'])
def create_entry(request):
    response = Response()
    data = get_request_data(request)
    title = data.get('title')
    content = data.get('content')
    category = data.get('category')
    date = data.get('date')
    create_category = data.get('createCategory')
    if create_category:
        category, created = EntryCategory.objects.get_or_create(
            category_name = data.get('category').lower()
        )
    else:
        category = EntryCategory.objects.get(category_uuid=category)
    requesting_user = token_is_valid(data.get('token'))
    if requesting_user and title and content and category and date:
        try:
            entry_instance = Entry.objects.create(
                title=title,
                content=content,
                category=category,
                date=date,
                owner=requesting_user
            )
            response.status_code = 200
            response.data = {'status': 'SUCCESS', 'entry_uuid': entry_instance.entry_uuid, 'category': {
                'name': category.category_name,
                'uuid': category.category_uuid
            }}
        except Exception as e:
            response.status_code = 500
            response.data = {'status': 'INTERNAL_ERROR'}
    else:
        response.status_code = 403
        response.data = {'status': 'NOT_ALLOWED'}
    return response

@api_view(['POST'])
def update_journal(request):
    response = Response()
    data = get_request_data(request)
    title = data.get('title')
    content = data.get('content')
    category = data.get('category')
    create_category = data.get('createCategory')
    if create_category:
        category, created = EntryCategory.objects.get_or_create(
            category_name = data.get('category').lower()
        )
    else:
        category = EntryCategory.objects.get(category_uuid=category)
    date = data.get('date')
    entry_uuid = data.get('uuid')
    requesting_user = token_is_valid(data.get('token'))
    if requesting_user and title and content and category and date and entry_uuid:
        try:
            entry_instance = Entry.objects.get(
                entry_uuid=entry_uuid
            )
            entry_instance.title = title
            entry_instance.content = content
            entry_instance.category = category
            entry_instance.date = date
            entry_instance.save()
            response.status_code = 200
            response.data = {'status': 'SUCCESS', 'category': {
                'name': category.category_name,
                'uuid': category.category_uuid
            }}
        except Exception as e:
            response.status_code = 500
            response.data = {'status': 'INTERNAL_ERROR'}
    else:
        response.status_code = 403
        response.data = {'status': 'NOT_ALLOWED'}
    return response

@api_view(['POST'])
def delete_journal(request):
    response = Response()
    data = get_request_data(request)
    entry_uuid = data.get('uuid')
    requesting_user = token_is_valid(data.get('token'))
    if requesting_user and entry_uuid:
        try:
            Entry.objects.get(entry_uuid=entry_uuid).delete()
            response.status_code = 200
            response.data = {'status': 'SUCCESS'}
        except Exception as e:
            response.status_code = 500
            response.data = {'status': 'INTERNAL_ERROR'}
    else:
        response.status_code = 403
        response.data = {'status': 'NOT_ALLOWED'}
    return response

@api_view(['POST'])
def filter_journal_entries(request):
    response = Response()
    data = get_request_data(request)
    filter_fields = data.get('filter_fields')
    requesting_user = token_is_valid(data.get('token'))
    if requesting_user:
        try:
            entries = FilterHelper(
                user=requesting_user,
                filter_fields=filter_fields
            ).results
            response.status_code = 200
            response.data = {'status': 'SUCCESS', 'data': entries}
        except:
            response.status_code = 500
            response.data = {'status': 'INTERNAL_ERROR'}
    else:
        response.status_code = 403
        response.data = {'status': 'NOT_ALLOWED'}
    return response

def token_is_valid(token):
    try:
        return UserModel.objects.get(
            user_ref=Token.objects.get(key=token).user
        )
    except:
        return False

def get_request_data(request):
    return request.data
