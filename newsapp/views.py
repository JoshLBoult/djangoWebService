from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from newsapp.models import Author, Story
import json

# Login handler
@csrf_exempt
def HandleLoginRequest(request):
    # Don't accept non-POST requests
    if (request.method != 'POST'):
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.content = 'Only POST requests are permitted for this resource\n'
        return http_bad_response

    # Get the login details provided
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    # Create http response object
    http_response = HttpResponse()
    http_response['Content-Type'] = 'text/plain'

    # Respond based on whether the user has been authenticated
    if user is not None:
        login(request, user)
        request.session.modified = True
        http_response.status_code = 200
        http_response.reason_phrase = 'OK'
        http_response.content = 'Welcome to The Josh Boult News Agency'
    else:
        http_response.status_code = 401
        http_response.reason_phrase = 'Unauthorized'
        http_response.content = 'Invalid login'

    return http_response

# Logout handler
@csrf_exempt
def HandleLogoutRequest(request):
    # Don't accept non-POST requests
    if (request.method != 'POST'):
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.content = 'Only POST requests are permitted for this resource\n'
        return http_bad_response

    # Logout
    logout(request)
    http_response = HttpResponse()
    http_response['Content-Type'] = 'text/plain'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    http_response.content = 'Goodbye, visit The Josh Boult News Agency soon!'
    return http_response


# Post a story, only available to logged in authors
@csrf_exempt
def HandlePostStoryRequest(request):
    # Don't accept non-POST requests
    if (request.method != 'POST'):
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.content = 'Only POST requests are permitted for this resource\n'
        return http_bad_response

    # Create response object
    http_response = HttpResponse()
    http_response['Content-Type'] = 'text/plain'

    # Check if user is logged in
    if request.user.is_authenticated:
        # Decode json data
        requestData = json.loads(request.data)
        # Create the story object and save to database
        author = Author.objects.get(user=request.user)
        headline = requestData['headline']
        category = requestData['category']
        region = requestData['region']
        details = requestData['details']
        s1 = Story(author=author, headline=headline, category=category, region=region,
        details=details)
        s1.save()
        http_response.status_code = 201
        http_response.reason_phrase = 'Created'
        http_response.content = 'Story added successfully'
        return http_response
    else:
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        http_response.content = 'User is not authenticated'

    return http_response


# Get a filtered story list from this news service, available to all users
@csrf_exempt
def HandleGetStoriesRequest(request):
    # Don't accept non-GET requests
    if (request.method != 'GET'):
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.content = 'Only GET requests are permitted for this resource\n'
        return http_bad_response

    # Retrieve information from the request
    requestData = json.loads(request.data)
    category = requestData['story_cat']
    region = requestData['story_region']
    date = requestData['story_date']

    # Get the total story list to begin with
    stories = Story.objects.all()

    # Now we check if there's something other than the default values to filter by
    if (category != '*'):
        stories = stories.filter(category=category)
    if (region != '*'):
        stories = stories.filter(region=region)
    if (date != '*'):
        stories = stories.filter(date__gte=date)

    # Check that stories still has some data
    if stories is not None:
        jsonList = []
        # Iterate through the story list as a dict
        for record in stories.values():
            # We need to get the author model as a dict first
            author = record['author']
            authorDict = author.values()
            # Withdraw the information and add to the JSON list
            item = {'key':record['id'], 'headline':record['headline'], 'story_cat':record['category'],
            'story_region':record['region'], 'author':authorDict['name'], 'date':record['date'],
            'details':record['details']}
            jsonList.append(item)
        payload = {'stories':jsonList}
        http_response = HttpResponse(json.dumps(payload))
        http_response.status_code = 200
        http_response.reason_phrase = 'OK'
        http_response['Content-Type'] = 'application/json'
        return http_response
    else:
        http_response = HttpResponse()
        http_response.status_code = 404
        http_response.reason_phrase = 'Not Found'
        http_response['Content-Type'] = 'text/plain'
        http_response.content = 'No stories match this filter'
        return http_response


# Delete a story as requested by a logged in user only
@csrf_exempt
def HandleDeleteStoryRequest(request):
    # Don't accept non-POST requests
    if (request.method != 'POST'):
        http_bad_response = HttpResponseBadRequest()
        http_bad_response['Content-Type'] = 'text/plain'
        http_bad_response.content = 'Only POST requests are permitted for this resource\n'
        return http_bad_response

    # Create response object
    http_response = HttpResponse()
    http_response['Content-Type'] = 'text/plain'

    # Check if user is logged in
    if request.user.is_authenticated:
        # Decode json data
        requestData = json.loads(request.data)
        # Delete the story object
        story_id = requestData['story_key']
        s1 = Story.objects.get(id=story_id)
        s1.delete()
        http_response.status_code = 201
        http_response.reason_phrase = 'Created'
        http_response.content = 'Story deleted successfully'
        return http_response
    else:
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        http_response.content = 'User is not authenticated'

    return http_response
















    #
