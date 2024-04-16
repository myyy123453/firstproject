# # @Author : Kql
# # @Time : 2023/8/18 11:49
# # @FileName : upload.py
# # @Blog ：https://blog.csdn.net/weixin_56175042
# from datetime import datetime
#
#
# from django.http import HttpResponse
# from django.core.files.uploadedfile import UploadedFile
# from django.shortcuts import render
#
# # from .forms import CSVFileForm
# import csv
#
# def upload_csv(request):
#     if request.method == 'POST':
#         form = CSVFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = request.FILES['file']
#             reader = csv.reader(csv_file)
#             # Process the CSV file, e.g., read and display the data
#             return HttpResponse("CSV file uploaded and processed.")
#         else:
#             return HttpResponse("Invalid CSV file. Please try again.")
#     else:
#         form = CSVFileForm()
#     return render(request, 'upload.html', {'form': form})
#
#
