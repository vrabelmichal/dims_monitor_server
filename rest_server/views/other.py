# https://www.django-rest-framework.org/api-guide/parsers/#fileuploadparser

# # views.py
# class FileUploadView(views.APIView):
#     parser_classes = [FileUploadParser]
#
#     def put(self, request, filename, format=None):
#         file_obj = request.data['file']
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(status=204)
#
# # urls.py
# urlpatterns = [
#     # ...
#     re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
# ]
