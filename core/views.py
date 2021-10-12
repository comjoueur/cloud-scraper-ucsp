import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

from core.forms import SearchForm


def search_token_directory(directory, token):
    for filename in os.listdir(directory):
        file_path = directory + filename

        with open(file_path) as file:
            for line in file:
                if line and line.split()[0] == token:
                    return line

    return " "


def search(request, *args, **kwargs):
    form = SearchForm()
    term = request.GET.get("term", "")
    if term:
        _, indices = search_token_directory(
            os.path.join(settings.BASE_DIR, "assets/inverted_index", ""), term
        ).split(" ")
        posts = []
        for index in indices.split(","):
            if not index:
                continue
            token, count = index.split(":")
            _, page_rank = search_token_directory(
                os.path.join(settings.BASE_DIR, "assets/page_rank", ""), token
            ).split(" ")
            page_rank = float(page_rank) if page_rank else 0
            posts.append(
                {
                    "id": token,
                    "count": count,
                    "url": "https://{}.s3.amazonaws.com/docs/{}".format(
                        settings.AWS_S3_BUCKET, token
                    ),
                    "rank": float(page_rank),
                }
            )

        return render(
            request,
            "search.html",
            {"form": form, "posts": sorted(posts, key=lambda d: -d["rank"])},
        )

    return HttpResponseRedirect("/?term=hola")
