from django.shortcuts import render
from app.youtube import ContentGenerator
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    if request.method == "POST":
        response = {
            "blog_post": "",
            "linkedin_post": "",
            "error": ""
        }
        body = json.loads(request.body)
        youtube_url = body.get("youtube_url")
        generate_linkedin_post = body.get("generate_linkedin_post")
        content_generator_obj = ContentGenerator(youtube_url)
        captions = content_generator_obj.generate_docs_from_transcript()
        if not captions:
            response["error"] = "No captions found"
            return JsonResponse(response)
        response["blog_post"] = content_generator_obj.generate_blog_post(captions)
        if generate_linkedin_post:
            response["linkedin_post"] = content_generator_obj.generate_linkedin_post(captions)
        return JsonResponse(response)
    return render(request, 'index.html')

def privacy_policy(request):
    return render(request, 'privacy.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')