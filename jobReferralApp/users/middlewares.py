# middlewares.py
import time
from django.core.cache import cache
from django.http import HttpResponseForbidden


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy địa chỉ IP của client
        ip = request.META.get('REMOTE_ADDR')

        # Key để lưu trữ số lần request của mỗi IP
        cache_key = f'rate_limit_{ip}'

        # Số lần request tối đa trong một khoảng thời gian
        limit = 100

        # Thời gian reset, ví dụ: mỗi 1 giờ
        reset_time = 60

        # Lấy số lần request đã gửi trong khoảng thời gian trước đó
        count = cache.get(cache_key, 0)

        # Kiểm tra số lần request
        if count >= limit:
            return HttpResponseForbidden("Rate limit exceeded. Please try again later.")

        # Tăng số lần request
        cache.set(cache_key, count + 1, reset_time)

        # Tiếp tục xử lý request
        response = self.get_response(request)

        return response
