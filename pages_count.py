total_results = 880265
data_points_per_page = 100

total_pages = total_results // data_points_per_page
if total_results % data_points_per_page != 0:
    total_pages += 1  # Add one more page for the remaining data

print(f'Total number of pages: {total_pages}')
